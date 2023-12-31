import atexit
from dataclasses import dataclass
from typing import Optional

import ctypes
import logging
import os
import pathlib
import sys
import time

import capstone
import kdmp_parser

import bochscpu
import bochscpu.cpu
import bochscpu.memory
import bochscpu.utils


cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)


def disass(state, va: int) -> capstone.CsInsn:
    global cs
    raw = bytes(bochscpu.memory.virt_read(state.cr3, va, 16))
    insn = next(cs.disasm(raw, va))
    return insn


emulation_end_address = 0

hvas: list[int] = []
dmp: Optional[kdmp_parser.KernelDumpParser] = None
session: Optional[bochscpu.Session] = None


@dataclass
class SessionPerf:
    start_time_ns: int = 0
    end_time_ns: int = 0
    executed_instruction: int = 0
    allocated_pages: int = 0

    @property
    def execution_time_ns(self) -> int:
        return self.end_time_ns - self.start_time_ns

    @property
    def execution_time(self) -> float:
        return self.execution_time_ns / 1_000_000_000

    @property
    def average(self) -> float:
        if not self.execution_time:
            return 0

        return self.executed_instruction / self.execution_time


perf = SessionPerf()


def hexdump(
    source: bytes, length: int = 0x10, separator: str = ".", base: int = 0x00
) -> str:
    result = []
    align = 0x8 * 2 + 2

    def chunk2hexstr(chunk: bytes):
        return " ".join(map(lambda x: f"{x:02X}", chunk))

    def chunk2ascii(chunk: bytes):
        return "".join([chr(b) if 0x20 <= b < 0x7F else separator for b in chunk])

    for i in range(0, len(source), length):
        chunk = bytearray(source[i : i + length])
        hexa = chunk2hexstr(chunk)
        text = chunk2ascii(chunk)
        result.append(f"{base + i:#0{align}x}   {hexa:<{3 * length}}    {text}")
    return os.linesep.join(result)


def missing_page_cb(pa):
    global session, dmp, hvas, perf
    assert dmp and session

    gpa = bochscpu.memory.align_address_to_page(pa)
    logging.debug(f"Missing GPA={gpa:#x}")

    if gpa in dmp.pages:
        # lazily handle missing page: first try to look into the dump, if found load it to mem
        hva = bochscpu.memory.allocate_host_page()
        page = dmp.read_physical_page(gpa)
        if hva and page:
            perf.allocated_pages += 1
            bochscpu.memory.page_insert(gpa, hva)
            bochscpu.memory.phy_write(gpa, page)
            logging.debug(f"{gpa=:#x} -> {hva=:#x}")
            hvas.append(hva)
            # we've successfully mapped it
            return

    # otherwise the page is really missing, bail
    session.stop()
    raise Exception


def exception_cb(
    sess: bochscpu.Session,
    cpu_id: int,
    vector: int,
    error_code: int,
):
    exception = bochscpu.cpu.ExceptionType(vector)
    match exception:
        case bochscpu.cpu.ExceptionType.BreakPoint:
            logging.info("[CPU#{cpu_id}] breakpoint hit")

        case bochscpu.cpu.ExceptionType.PageFault:
            state = sess.cpu.state

            # see Intel 3A - 4.7
            reason = ""
            if error_code & (1 << 15):
                reason = "SGX related"
            else:
                reason += (
                    "page-level protection violation"
                    if error_code & 1
                    else "non-present page"
                )
                reason += ", write access" if error_code & (1 << 1) else ", read access"
                reason += (
                    ", user mode" if error_code & (1 << 2) else ", supervisor mode"
                )
                reason += (
                    ", instruction fetch"
                    if error_code & (1 << 4)
                    else ", not an instruction fetch"
                )

            logging.warning(
                f"[CPU#{cpu_id}] pagefault on VA={state.cr2:#016x} at IP={state.rip:#016x}: {reason=}"
            )

        case _:
            logging.error(
                f"[CPU#{cpu_id}] received exception({exception=}, {error_code=:#x}) "
            )
    sess.stop()


def before_execution_cb(sess: bochscpu.Session, cpu_id: int, _: int):
    global perf
    perf.executed_instruction += 1
    state = sess.cpu.state
    insn = disass(state, state.rip)
    logging.debug(
        f"[CPU#{cpu_id}] PC={state.rip:#x} {insn.bytes.hex()} - {insn.mnemonic} {insn.op_str}"
    )


def after_execution_cb(sess: bochscpu.Session, cpu_id: int, _: int):
    global emulation_end_address

    if not emulation_end_address:
        return

    if emulation_end_address == sess.cpu.state.rip:
        logging.info(
            f"[CPU#{cpu_id}] Reaching end address @ {emulation_end_address}, ending emulation"
        )
        sess.stop()


def resolve_function(symbol: str) -> int:
    kernel32 = ctypes.windll.kernel32
    kernel32.GetModuleHandleW.argtypes = [ctypes.c_wchar_p]
    kernel32.GetModuleHandleW.restype = ctypes.c_void_p
    kernel32.GetProcAddress.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    kernel32.GetProcAddress.restype = ctypes.c_void_p

    dll, func = symbol.split("!", 1)
    if not dll.lower().endswith(".dll"):
        dll += ".dll"
    logging.info(f"Looking up {func} in {dll}")
    handle = kernel32.GetModuleHandleW(dll)
    address: int = kernel32.GetProcAddress(handle, func.encode())
    if not address:
        raise RuntimeError(f"Failed to resolve {symbol}")
    logging.info(f"Resolved '{symbol:s}' -> {address:#x}")
    return address


def emulate(dmp_path: pathlib.Path):
    global session, dmp

    assert session is None

    logging.info(f"Parsing {dmp_path}")
    dmp = kdmp_parser.KernelDumpParser(dmp_path)
    assert dmp

    logging.info(f"Successfully parsed {dmp_path}")
    logging.debug(f"{dmp=}")

    session = bochscpu.Session()
    session.missing_page_handler = missing_page_cb

    logging.debug("Preparing CPU state")
    state = bochscpu.State()
    bochscpu.cpu.set_long_mode(state)

    logging.debug("Enabling MMX (SSE/AVX) instructions")
    cr0 = bochscpu.utils.cpu.CR0(state.cr0)
    cr4 = bochscpu.utils.cpu.CR4(state.cr4)
    xcr0 = bochscpu.utils.cpu.XCR0(state.xcr0)
    # See AMD Vol2 - 11.3
    cr0.MP = True
    cr0.EM = False
    cr4.OSFXSR = True
    cr4.OSXSAVE = True
    # See AMD Vol2 - 11.5.2
    xcr0.x87 = True
    xcr0.SSE = True
    xcr0.YMM = True

    # TODO use bdump.js::regs.json instead
    logging.debug(f"Setting {cr0=:}")
    logging.debug(f"Setting {cr4=:}")
    logging.debug(f"Setting {xcr0=:}")
    state.cr0 = int(cr0)
    state.cr4 = int(cr4)
    state.xcr0 = int(xcr0)

    cr3 = dmp._KernelDumpParser__dump.GetDirectoryTableBase()  # type: ignore #  HACK
    logging.debug(f"Setting CR3={cr3:#x}")
    state.cr3 = cr3

    logging.debug(f"Setting the flag register")
    state.rflags = dmp.context.ContextFlags

    logging.debug(f"Setting the other GPRs")
    for regname in (
        "rax",
        "rbx",
        "rcx",
        "rdx",
        "rsi",
        "rdi",
        "rip",
        "rsp",
        "rbp",
        "r8",
        "r9",
        "r10",
        "r11",
        "r12",
        "r13",
        "r14",
        "r15",
    ):
        value = int(getattr(dmp.context, regname.capitalize()))
        setattr(state, regname, value)

    logging.debug(f"Setting the segment selectors")
    _cs = bochscpu.Segment()
    _cs.base = 0
    _cs.limit = 0xFFFF_FFFF
    _cs.selector = dmp.context.SegCs
    _cs_attr = bochscpu.cpu.SegmentFlags()
    _cs_attr.A = True
    _cs_attr.R = True
    _cs_attr.E = True
    _cs_attr.S = True
    _cs_attr.P = True
    _cs_attr.L = True
    _cs.attr = int(_cs_attr)
    _ds = bochscpu.Segment()
    _ds.base = 0
    _ds.limit = 0xFFFF_FFFF
    _ds.selector = dmp.context.SegDs
    _ds.attr = 0xCF3
    _es = bochscpu.Segment()
    _es.base = 0
    _es.limit = 0xFFFF_FFFF
    _es.selector = dmp.context.SegEs
    _es.attr = 0xCF3
    _ss = bochscpu.Segment()
    _ss.base = 0
    _ss.limit = 0xFFFF_FFFF
    _ss.selector = dmp.context.SegSs
    _ss.attr = 0xCF3
    _fs = bochscpu.Segment()
    _fs.base = 0
    _fs.limit = 0xFFFF_FFFF
    _fs.selector = dmp.context.SegFs
    _fs.present = True
    _fs.attr = 0x4F3
    _gs = bochscpu.Segment()
    _gs.base = 0
    _gs.limit = 0xFFFF_FFFF
    _gs.selector = dmp.context.SegGs
    _gs.present = True
    _gs.attr = 0xCF3

    state.ss = _ss
    state.cs = _cs
    state.ds = _ds
    state.es = _es
    state.fs = _fs
    state.gs = _gs

    _idtr = bochscpu.GlobalSegment()
    _idtr.base = 0xFFFFF8065ED68000
    _idtr.limit = 0x0FFF
    state.idtr = _idtr

    _gdtr = bochscpu.GlobalSegment()
    _gdtr.base = 0xFFFFF8065ED6AFB0
    _gdtr.limit = 0x57
    state.gdtr = _gdtr

    _tr = bochscpu.Segment()
    _tr.base = 0x00000005ED69000
    _tr.limit = 0x67
    _tr.selector = 0x40
    _tr.attr = 0x8B

    # TODO missing kernel_gs_base
    # TODO missing gdtr/ldtr/idtr/tr
    # TODO missing simd/fpu

    # RIP should be at an int3 instruction, so patch it so we can resume execution
    state.rip += 1

    logging.debug(f"Apply the created state to the session CPU")
    session.cpu.state = state

    logging.debug("Preparing hooks")
    hook = bochscpu.Hook()
    hook.exception = exception_cb
    hook.before_execution = before_execution_cb
    hook.after_execution = after_execution_cb

    logging.debug("Initial register state")
    bochscpu.utils.dump_registers(session.cpu.state, True)

    logging.debug("Let's go baby!")

    perf.start_time_ns = int(time.time_ns())
    session.run(
        [
            hook,
        ]
    )

    session.stop()
    perf.end_time_ns = int(time.time_ns())

    logging.debug("Final register state")
    bochscpu.utils.dump_registers(session.cpu.state, True)

    logging.debug(f"{perf=}")
    logging.info(f"{perf.average=} insn/s")


def clean():
    logging.debug("Cleanup")
    for hva in hvas:
        bochscpu.memory.release_host_page(hva)


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
    arg = pathlib.Path(sys.argv[1]).resolve()
    assert arg.exists()
    emulate(arg)
    atexit.register(clean)
