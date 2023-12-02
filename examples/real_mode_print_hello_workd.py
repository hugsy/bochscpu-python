import logging
import os

import keystone
import bochscpu
import bochscpu.cpu
import bochscpu.memory
import bochscpu.utils

PAGE_SIZE = bochscpu.utils.PAGE_SIZE

def hexdump(
    source: bytes, length: int = 0x10, separator: str = ".", base: int = 0x00
) -> str:
    result = []
    align = length + 2

    for i in range(0, len(source), length):
        chunk = bytearray(source[i : i + length])
        hexa = " ".join(map(lambda x: f"{x:02X}", chunk))
        text = "".join([chr(b) if 0x20 <= b < 0x7F else separator for b in chunk])
        result.append(f"{base + i:#0{align}x}   {hexa:<{3 * length}}    {text}")
    return os.linesep.join(result)


def missing_page_cb(gpa: int):
    raise Exception(f"missing_page_cb({gpa=:#x})")


def before_execution_cb(sess: bochscpu.Session, cpu_id: int, _: int):
    logging.debug(f"[CPU#{cpu_id}] before PC={sess.cpu.rip:#08x}")


def after_execution_cb(sess: bochscpu.Session, cpu_id: int, _: int):
    logging.debug(f"[CPU#{cpu_id}] after PC={sess.cpu.rip:#08x}")


def cache_cntrl_cb(sess: bochscpu.Session, a1: int, a2: int):
    logging.debug("in cache_cntrl_cb")


def clflush_cb(sess: bochscpu.Session, a1: int, a2: int, a3: int):
    logging.debug("in clflush_cb")


def cnear_branch_not_taken_cb(sess: bochscpu.Session, cpu_id: int, before: int, after: int):
    logging.debug(f"in cnear_branch_not_taken_cb, {cpu_id=:#x} {before=:#x} {after=:#x}")


def cnear_branch_taken_cb(sess: bochscpu.Session, cpu_id: int, before: int, after: int):
    logging.debug(f"in cnear_branch_taken_cb, {cpu_id=:#x} {before=:#x} {after=:#x}")


def far_branch_cb(
    sess: bochscpu.Session, a1: int, a2: int, a3: int, a4: int, a5: int, a6: int
):
    logging.debug("far_branch_cb")


def hlt_cb(sess: bochscpu.Session, reason: int):
    logging.debug(f"in hlt_cb, {reason=:#x}")
    sess.stop()


def hw_interrupt_cb(sess: bochscpu.Session, a1: int, a2: int, a3: int, a4: int):
    logging.debug("in hw_interrupt_cb")


def inp_cb(sess: bochscpu.Session, a1: int, a2: int):
    logging.debug("in inp_cb")


def inp2_cb(sess: bochscpu.Session, a1: int, a2: int, a3: int):
    logging.debug("in inp2_cb")


def interrupt_cb(sess: bochscpu.Session, cpu_id: int, int_num: int):
    logging.debug(f"in interrupt_cb, {cpu_id=} received {int_num=:#x}")
    mode = sess.cpu.state.rax >> 8
    match int_num, mode:
        case 0x10, 0x0e:
            # https://en.wikipedia.org/wiki/INT_10H
            char = chr(sess.cpu.state.rax & 0xff)
            # pg_num = sess.cpu.state.rbx & 0xf0
            # color = sess.cpu.state.rbx & 0x0f
            print(f"{char=}")
        case _:
            logging.warning(f"[CPU#{cpu_id}] unsupported interrupt {int_num}")


def lin_access_cb(
    sess: bochscpu.Session, a1: int, a2: int, a3: int, a4: int, a5: int, a6: int
):
    logging.debug("in lin_access_cb")


def mwait_cb(sess: bochscpu.Session, a1: int, a2: int, a3: int, a4: int):
    logging.debug("in mwait_cb")


def opcode_cb(
    sess: bochscpu.Session, a1: int, a2: int, a3: int, a4: int, a5: bool, a6: bool
):
    logging.debug("in opcode_cb")


def outp_cb(sess: bochscpu.Session, a1: int, a2: int, a3: int):
    logging.debug("in outp_cb")


def phy_access_cb(sess: bochscpu.Session, a1: int, a2: int, a3: int, a4: int, a5: int):
    logging.debug("in phy_access_cb")


def prefetch_hint_cb(sess: bochscpu.Session, a1: int, a2: int, a3: int, a4: int):
    logging.debug("in prefetch_hint_cb")


def repeat_iteration_cb(sess: bochscpu.Session, a1: int, a2: int):
    logging.debug("in repeat_iteration_cb")


def reset_cb(sess: bochscpu.Session, a1: int, a2: int):
    logging.debug("in reset_cb")


def tlb_cntrl_cb(sess: bochscpu.Session, a1: int, a2: int, a3: int):
    logging.debug("in tlb_cntrl_cb")


def ucnear_branch_cb(sess: bochscpu.Session, cpu_id: int, a2: int, a3: int, a4: int):
    logging.debug(f"in ucnear_branch_cb, {cpu_id=:#x} {a2=:#x} {a3=:#x}  {a4=:#x}")


def vmexit_cb(sess: bochscpu.Session, a1: int, a2: int, a3: int):
    logging.debug("in vmexit_cb")


def wrmsr_cb(sess: bochscpu.Session, a1: int, a2: int, a3: int):
    logging.debug("in wrmsr_cb")


def exception_cb(
    sess: bochscpu.Session,
    cpu_id: int,
    vector: int,
    error_code: int,
):
    match (vector, error_code):
        case _:
            v = bochscpu.cpu.ExceptionType(vector)
            logging.warning(f"[CPU#{cpu_id}] Received exception({v}, {error_code=:d}) ")
    sess.stop()


def emulate(code_str: str):
    #
    # Use Keystone to compile the assembly
    #
    ks = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_16)
    code, _ = ks.asm(code_str)
    assert isinstance(code, list)
    code = bytes(code)
    logging.debug(f"Compiled {len(code)} bytes")
    code = code.ljust(PAGE_SIZE, b"\xcc") # Make sure we hit an exception, helpful for debug
    assert len(code) == PAGE_SIZE

    #
    # Create the pages
    #
    logging.debug("Allocating host pages")
    code_hva = bochscpu.memory.allocate_host_page()
    code_gpa = 0x0000_1000
    bochscpu.memory.page_insert(code_gpa, code_hva)
    bochscpu.memory.phy_write(code_gpa, bytearray(code))

    data_hva = bochscpu.memory.allocate_host_page()
    data_gpa = 0x0000_2000
    bochscpu.memory.page_insert(data_gpa, data_hva)
    bochscpu.memory.phy_write(data_gpa, bytearray(b"ello world!"))

    stack_hva = bochscpu.memory.allocate_host_page()
    stack_gpa = 0x0000_8000
    bochscpu.memory.page_insert(stack_gpa, stack_hva)

    #
    # Intel 3A - 3.4.3
    # > For virtually any kind of program execution to take place, at least the code-segment (CS),
    # > data-segment (DS), and stack-segment (SS) registers must be loaded with valid segment selectors
    #
    logging.debug("Setting up CPU segments")

    # CS segment
    _cs = bochscpu.Segment()
    _cs.base = code_gpa
    _cs.limit = PAGE_SIZE
    _cs.selector = 6 << 3| 0 << 2 | 0 # DescriptorTable[6], TI=0->GDT, RPL=0
    cs_attr = bochscpu.cpu.SegmentFlags()
    cs_attr.P = True
    cs_attr.E = True
    cs_attr.DB = False
    cs_attr.G = False
    cs_attr.S = True
    cs_attr.DPL = 0
    cs_attr.R = True
    _cs.attr = int(cs_attr)
    _cs.present = True

    # SS segment
    _ss = bochscpu.Segment()
    _ss.present = True
    _ss.base = stack_gpa
    _ss.limit = PAGE_SIZE >> 4 # Granularity is 16b (D off)
    _ss.selector = 8 << 3| 0 << 2 | 0 # DescriptorTable[8], TI=0->GDT, RPL=0
    ss_attr = bochscpu.cpu.SegmentFlags()
    ss_attr.P = True
    ss_attr.DB = False
    ss_attr.E = False
    ss_attr.D = True
    ss_attr.W = True
    ss_attr.A = True
    ss_attr.S = True
    ss_attr.DPL = 0
    _ss.attr = int(ss_attr)

    # DS segment
    _ds = bochscpu.Segment()
    _ds.present = True
    _ds.base = data_gpa
    _ds.limit = PAGE_SIZE
    _ds.selector = 10 << 3| 0 << 2 | 0 # DescriptorTable[10], TI=0->GDT, RPL=0
    ds_attr = bochscpu.cpu.SegmentFlags()
    ds_attr.P = True
    ds_attr.E = False
    ds_attr.D = False
    ds_attr.W = True
    ds_attr.G = False
    ds_attr.S = True
    _ds.attr = int(ds_attr)

    #
    # Create the VM session, add the missing page handler
    #
    sess = bochscpu.Session()
    sess.missing_page_handler = missing_page_cb

    #
    # And initialize a CPU state
    #
    state = bochscpu.State()
    bochscpu.cpu.set_real_mode(state)

    #
    # Assign segment to the state, CS, DS and SS are always required
    #
    state.ds = _ds


    # The SP will be at ss:[0x0800]
    state.ss = _ss
    state.rsp = 0x0800

    # The PC will be at cs:[0x0000]
    state.cs = _cs
    state.rip = 0x0000

    #
    # Ok! Our CPU is now in valid state for paging allowing to resolve logical addresses
    # Apply the state to the emulation session
    #
    logging.debug("Applying CPU state")
    sess.cpu.state = state

    #
    # For demo purposes, we add mock callbacks for everything bochs can instrument
    #
    hook = bochscpu.Hook()
    hook.after_execution = after_execution_cb
    hook.before_execution = before_execution_cb
    hook.cache_cntrl = cache_cntrl_cb
    hook.clflush = clflush_cb
    hook.cnear_branch_not_taken = cnear_branch_not_taken_cb
    hook.cnear_branch_taken = cnear_branch_taken_cb
    hook.exception = exception_cb
    hook.far_branch = far_branch_cb
    hook.hlt = hlt_cb
    hook.hw_interrupt = hw_interrupt_cb
    hook.inp = inp_cb
    hook.interrupt = interrupt_cb
    hook.lin_access = lin_access_cb
    hook.mwait = mwait_cb
    hook.opcode = opcode_cb
    hook.outp = outp_cb
    hook.phy_access = phy_access_cb
    hook.prefetch_hint = prefetch_hint_cb
    hook.repeat_iteration = repeat_iteration_cb
    hook.reset = reset_cb
    hook.tlb_cntrl = tlb_cntrl_cb
    hook.ucnear_branch = ucnear_branch_cb
    hook.vmexit = vmexit_cb
    hook.wrmsr = wrmsr_cb

    hooks = [hook]

    logging.debug(
        f"Starting emulation at cs:{state.rip:#08x} with {len(hooks)} hookchain(s)"
    )
    if logging.getLogger().isEnabledFor(logging.DEBUG):
        bochscpu.utils.dump_registers(sess.cpu.state)
    sess.run(hooks)
    sess.stop()

    logging.debug(f"Stopped emulation at cs:{sess.cpu.rip:#08x}, final register state")
    if logging.getLogger().isEnabledFor(logging.DEBUG):
        bochscpu.utils.dump_registers(sess.cpu.state)

    #
    # Cleanup
    #
    logging.debug("Cleaning up")
    bochscpu.memory.release_host_page(code_hva)
    bochscpu.memory.release_host_page(stack_hva)
    bochscpu.memory.release_host_page(data_hva)


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)-7s - %(message)s", level=logging.DEBUG)
    code = """
print:
    push ax

printchar:
    lodsb
    test al, al
    je end

    mov ah, 0x0E
    int 0x10

    inc si
    jmp printchar

end:
    pop ax
    hlt
"""
    emulate(code)
