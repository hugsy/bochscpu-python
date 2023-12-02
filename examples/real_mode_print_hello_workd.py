import logging
import sys

import keystone
import bochscpu
import bochscpu.cpu
import bochscpu.memory
import bochscpu.utils

PAGE_SIZE = bochscpu.utils.PAGE_SIZE


def missing_page_cb(gpa: int):
    raise Exception(f"missing_page_cb({gpa=:#x})")


def before_execution_cb(sess: bochscpu.Session, cpu_id: int, insn: int):
    logging.debug(f"[CPU#{cpu_id}] before PC={sess.cpu.rip:#08x}")


def after_execution_cb(sess: bochscpu.Session, cpu_id: int, insn: int):
    logging.debug(f"[CPU#{cpu_id}] after PC={sess.cpu.rip:#08x}")


def cnear_branch_not_taken_cb(sess: bochscpu.Session, cpu_id: int, before: int, after: int):
    logging.debug(f"in cnear_branch_not_taken_cb, {cpu_id=:#x} {before=:#x} {after=:#x}")


def cnear_branch_taken_cb(sess: bochscpu.Session, cpu_id: int, before: int, after: int):
    logging.debug(f"in cnear_branch_taken_cb, {cpu_id=:#x} {before=:#x} {after=:#x}")


def hlt_cb(sess: bochscpu.Session, reason: int):
    logging.debug(f"in hlt_cb, {reason=:#x}")
    sess.stop()


def interrupt_cb(sess: bochscpu.Session, cpu_id: int, int_num: int):
    logging.debug(f"in interrupt_cb, {cpu_id=} received {int_num=:#x}")
    mode = sess.cpu.state.rax >> 8
    match int_num, mode:
        case 0x10, 0x0e:
            #
            # This is the main juice of the emulated interruption
            # ref: https://en.wikipedia.org/wiki/INT_10H
            #
            char = chr(sess.cpu.state.rax & 0xff)
            print(f"{char}", end="")

            #
            # We've emulated a print, let's cheap and just resume executing at the next IP
            # (avoid creating an IDT etc.)
            #
            sess.cpu.rip += 1

        case _:
            logging.warning(f"[CPU#{cpu_id}] unsupported interrupt {int_num}")


def exception_cb(
    sess: bochscpu.Session,
    cpu_id: int,
    vector: int,
    error_code: int,
):
    match (vector, error_code):
        case _:
            logging.warning(f"[CPU#{cpu_id}] Received exception({bochscpu.cpu.ExceptionType(vector)}, {error_code=:d}) ")
    sess.stop()


def emulate(code_str: str, data: bytes):
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
    bochscpu.memory.phy_write(data_gpa, bytearray(data))

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
    # We also set the interrupt table
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
    # For demo purposes, we add a few callbacks but they're not all useful.
    #
    hook = bochscpu.Hook()
    hook.after_execution = after_execution_cb
    hook.before_execution = before_execution_cb
    hook.cnear_branch_not_taken = cnear_branch_not_taken_cb
    hook.cnear_branch_taken = cnear_branch_taken_cb
    hook.exception = exception_cb
    hook.hlt = hlt_cb
    hook.interrupt = interrupt_cb

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
    if "--debug" in sys.argv[1:]:
        logging.basicConfig(format="%(levelname)-7s - %(message)s", level=logging.DEBUG)
    else:
        logging.basicConfig(format="%(levelname)-7s - %(message)s", level=logging.INFO)
    print_msg_asm = """
_start:
    push ax

printchar:
    lodsb
    test al, al
    je end

    mov ah, 0x0E
    int 0x10

    nop
    jmp printchar

end:
    pop ax
    hlt
"""
    emulate(print_msg_asm, b"Hello 16-bit assembly!\n\0")
