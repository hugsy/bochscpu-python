import ctypes
import logging
import os
import pathlib
import sys
import enum

import capstone
import udmp_parser

import bochscpu
import bochscpu.cpu
import bochscpu.memory
import bochscpu.utils


kernel32 = ctypes.windll.kernel32
kernel32.GetModuleHandleW.argtypes = [ctypes.c_wchar_p]
kernel32.GetModuleHandleW.restype = ctypes.c_void_p
kernel32.GetProcAddress.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
kernel32.GetProcAddress.restype = ctypes.c_void_p

PAGE_SIZE = bochscpu.utils.PAGE_SIZE
PA_START_ADDRESS = 0x100_0000
PML4_ADDRESS = 0x10_0000
MEM_FREE = 0x00010000
PAGE_NOACCESS = 0x01


class Permission(enum.IntEnum):
    CODE = 0
    RW = 1


cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

emulation_end_address = 0


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


def missing_page_cb(gpa):
    raise Exception(f"missing_page_cb({gpa=:#x})")


def phy_access_cb(
    sess: bochscpu.Session, cpu_id: int, lin: int, phy: int, len: int, rw: int
):
    logging.debug(f"{lin=:#x} -> {phy=:#x}, {len=:#x}, {bool(rw)=}")


def exception_cb(
    sess: bochscpu.Session,
    cpu_id: int,
    vector: int,
    error_code: int,
):
    excpt = bochscpu.cpu.ExceptionType(vector)
    match excpt:
        case bochscpu.cpu.ExceptionType.BreakPoint:
            logging.info("breakpoint hit")

        case bochscpu.cpu.ExceptionType.PageFault:
            logging.warning(
                f"pagefault on VA={sess.cpu.cr2:#016x} at IP={sess.cpu.rip:#016x}"
            )

        case _:
            logging.error(
                f"cpu#{cpu_id} received exception({excpt=}, {error_code=:d}) "
            )
    sess.stop()


def before_execution_cb(sess: bochscpu.Session, cpu_id: int, _: int):
    state = sess.cpu.state
    raw = bytes(bochscpu.memory.virt_read(PML4_ADDRESS, state.rip, 16))
    insn = next(cs.disasm(raw, state.rip))
    logging.debug(
        f"[CPU#{cpu_id}] PC={state.rip:#x} {insn.bytes.hex()} - {insn.mnemonic} {insn.op_str}"
    )


def after_execution_cb(sess: bochscpu.Session, cpu_id: int, _: int):
    global emulation_end_address
    if not emulation_end_address:
        return

    if emulation_end_address == sess.cpu.state.rip:
        logging.info(
            f"Reaching end address @ {emulation_end_address}, ending emulation"
        )
        sess.stop()


def convert_region_protection(protect: int) -> int:
    match protect:
        case 0x02:  # PAGE_READONLY
            return Permission.RW
        case 0x04:  # PAGE_READWRITE
            return Permission.RW
        case 0x08:  # PAGE_WRITECOPY
            return Permission.RW
        case 0x10:  # PAGE_EXECUTE
            return Permission.CODE
        case 0x20:  # PAGE_EXECUTE_READ
            return Permission.CODE
        case 0x40:  # PAGE_EXECUTE_READWRITE
            return Permission.CODE
        case 0x80:  # PAGE_EXECUTE_WRITECOPY
            return Permission.RW

    # logging.warning(f"Unknown {protect=:#x})")
    return -1


def switch_to_thread(state: bochscpu.State, thread: udmp_parser.Thread):
    assert isinstance(thread.Context, udmp_parser.Context64)

    #
    # AMD Vol2 - A.1 System Software MSRs
    #
    FSBase = 0xC000_0100
    GSBase = 0xC000_0101
    KernelGSBase = 0xC000_0102

    logging.debug(f"Switching context to {thread}")
    _cs = bochscpu.Segment()
    _cs.base = 0
    _cs.limit = 0xFFFF_FFFF
    _cs.selector = thread.Context.SegCs
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
    _ds.selector = thread.Context.SegDs
    _ds.attr = 0xCF3

    _es = bochscpu.Segment()
    _es.base = 0
    _es.limit = 0xFFFF_FFFF
    _es.selector = thread.Context.SegEs
    _es.attr = 0xCF3
    _ss = bochscpu.Segment()
    _ss.base = 0
    _ss.limit = 0xFFFF_FFFF
    _ss.selector = thread.Context.SegSs
    _ss.attr = 0xCF3
    # AMD Vol2 - 4.5.3
    # > In 64-bit mode, FS-segment and GS-segment overrides are not checked for limit or attributes. Instead,
    # > the processor checks that all virtual-address references are in canonical form
    _fs = bochscpu.Segment()
    _fs.base = 0
    _fs.limit = 0xFFFF_FFFF
    _fs.selector = thread.Context.SegFs
    _fs.present = True
    _fs.attr = 0xCF3
    _gs = bochscpu.Segment()
    _gs.base = thread.Teb
    _gs.limit = 0x0000_0FFF
    _gs.selector = thread.Context.SegGs
    _gs.present = True
    _gs.attr = 0x4F3

    state.ss = _ss
    state.cs = _cs
    state.ds = _ds
    state.es = _es
    state.fs = _fs
    state.gs = _gs

    state.rip = thread.Context.Rip
    state.rsp = thread.Context.Rsp
    return


def call_function(
    sess: bochscpu.Session,
    start_address: int,
    end_address: int,
    args: list[int],
) -> None:
    global emulation_end_address

    state = sess.cpu.state
    state.rip = start_address

    if len(args) >= 1:
        state.rcx = args[0]
    if len(args) >= 2:
        state.rdx = args[1]
    if len(args) >= 3:
        state.r8 = args[2]
    if len(args) >= 4:
        state.r9 = args[3]

    logging.debug("Preparing hooks")
    hook = bochscpu.Hook()
    hook.exception = exception_cb
    hook.before_execution = before_execution_cb
    hook.after_execution = after_execution_cb

    logging.debug("Preparing emulation environment")
    sess.cpu.state = state

    if logging.getLogger().level == logging.DEBUG:
        logging.debug("Dumping initial register state")
        bochscpu.utils.dump_registers(sess.cpu.state)

    emulation_end_address = end_address

    logging.debug("Start emulation")
    sess.run(
        [
            hook,
        ]
    )

    if logging.getLogger().level == logging.DEBUG:
        logging.debug("Dumping final register state")
        bochscpu.utils.dump_registers(sess.cpu.state)
    return


def resolve_function(symbol: str) -> int:
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


def emulate(dmp):
    dmp_path = pathlib.Path(dmp)
    logging.info(f"Parsing {dmp_path}")
    dmp = udmp_parser.UserDumpParser()
    assert dmp.Parse(dmp_path)
    logging.info(f"Successfully parsed {dmp_path}")

    sess = bochscpu.Session()
    sess.missing_page_handler = missing_page_cb

    logging.debug("Preparing page table")
    pt = bochscpu.memory.PageMapLevel4Table()
    pa = PA_START_ADDRESS
    pgnb = 0

    for _, region in dmp.Memory().items():
        # logging.debug(f"mapping {region=}")
        if region.State == MEM_FREE or region.Protect == PAGE_NOACCESS:
            continue
        start, end = region.BaseAddress, region.BaseAddress + region.RegionSize
        for va in range(start, end, PAGE_SIZE):
            flags = convert_region_protection(region.Protect)
            if flags < 0:
                continue
            pt.insert(va, pa, flags)
            assert pt.translate(va) == pa
            hva = bochscpu.memory.allocate_host_page()
            bochscpu.memory.page_insert(pa, hva)
            print(f"\bmapped {va=:#x} to {pa=:#x} with {flags=}\r", end="")
            pa += PAGE_SIZE
            pgnb += 1

    logging.debug(f"{pgnb} pages inserted")

    buffer_hva = bochscpu.memory.allocate_host_page()
    buffer_pa = 0x4100_0000
    buffer_va = 0x41_0000_0000
    pt.insert(buffer_va, buffer_pa, Permission.RW)
    bochscpu.memory.page_insert(buffer_pa, buffer_hva)

    stack_hva = bochscpu.memory.allocate_host_page()
    stack_pa = 0x4200_0000
    stack_va = 0x42_0000_0000
    pt.insert(stack_va, stack_pa, Permission.RW)
    bochscpu.memory.page_insert(stack_pa, stack_hva)

    logging.debug(f"Committing {pgnb} pages")
    layout = pt.commit(PML4_ADDRESS)
    for hva, gpa in layout:
        bochscpu.memory.page_insert(gpa, hva)
        evaled_hva = bochscpu.memory.phy_translate(gpa)
        assert evaled_hva == hva, f"{evaled_hva=:#x} == {hva=:#x}"
        # print(f"mapped {gpa=:#x} to {hva=:#x}\r", end="")

    # bochscpu.utils.dump_page_table(PML4_ADDRESS)

    logging.debug("Copy memory content")
    for _, region in dmp.Memory().items():
        if region.State == MEM_FREE or region.AllocationProtect == PAGE_NOACCESS:
            continue
        start, end = region.BaseAddress, region.BaseAddress + region.RegionSize
        content = dmp.ReadMemory(start, end)
        assert content is not None
        content = bytes(content)
        bochscpu.memory.virt_write(PML4_ADDRESS, start, bytes(content))
        del content

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

    logging.debug(f"Setting {cr0=:}")
    logging.debug(f"Setting {cr4=:}")
    logging.debug(f"Setting {xcr0=:}")
    state.cr0 = int(cr0)
    state.cr4 = int(cr4)
    state.xcr0 = int(xcr0)

    logging.debug(f"Setting PML4 to {PML4_ADDRESS:#x}")
    state.cr3 = PML4_ADDRESS

    threads = dmp.Threads()
    tids = list(threads.keys())
    switch_to_thread(state, threads[tids[0]])

    sess.cpu.state = state

    fn_sym = "cryptbase!SystemFunction036"
    logging.debug(f"Resolving '{fn_sym}'")
    fn_start = resolve_function(fn_sym)
    fn_end = fn_start + 0x1C
    logging.info(f"{fn_sym} found at {fn_start:#x}")

    call_function(
        sess,
        fn_start,
        fn_end,
        [
            buffer_va,
            16,
        ],
    )
    data = bytes(bochscpu.memory.virt_read(PML4_ADDRESS, buffer_va, 0x10))
    print(hexdump(data))

    bochscpu.memory.release_host_page(stack_pa)
    bochscpu.memory.release_host_page(buffer_pa)


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.WARNING)
    arg = sys.argv[1]
    emulate(arg)
