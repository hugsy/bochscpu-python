import logging

import bochscpu
import bochscpu.cpu
import bochscpu.memory
import bochscpu.utils


def missing_page_cb(gpa: int):
    """Edit this function to change the page fault behavior
    Args:
        gpa (int): the physical address of where the page fault occured
    """
    raise RuntimeError(f"missing_page_cb({gpa=:#x})")


def before_execution_cb(sess: bochscpu.Session, cpu_id: int, _: int):
    """Default callback for `before_execution_cb`

    The  callback  is  called  each time, when Bochs simulator starts a new
    instruction execution. In case of repeat instruction the callback will
    be called only once before the first iteration will be started.
    """
    logging.debug(f"[CPU#{cpu_id}] before PC={sess.cpu.rip:#x}")


def after_execution_cb(sess: bochscpu.Session, cpu_id: int, _: int):
    """Default callback for `after_execution_cb`

    The  callback  is  called  each time, when Bochs simulator finishes any
    instruction execution. In case of repeat instruction the callback will
    be called only once after all repeat iterations.
    """
    logging.debug(f"[CPU#{cpu_id}] after PC={sess.cpu.rip:#x}")


def exception_cb(
    sess: bochscpu.Session,
    cpu_id: int,
    vector: int,
    error_code: int,
):
    """Default callback for `exception`

    The callback is called each time, when Bochs simulator executes an exception.
    """
    whatwhat = bochscpu.cpu.ExceptionType(vector)
    match (vector, error_code):
        case _:
            logging.warning(
                f"cpu#{cpu_id} received exception({whatwhat}, {error_code=:d}) "
            )
    sess.stop()


def cache_cntrl_cb(sess: bochscpu.Session, cpu_id: int, what: int):
    """Default callback for `cache_cntrl`

    The  callback  is  called each time, when Bochs simulator executes a cache/tlb
    control instruction.
    """
    whatwhat = bochscpu.CacheControlType(what)
    logging.debug(f"cache_cntrl_cb({sess=}, {cpu_id=}, {whatwhat})")


def clflush_cb(sess: bochscpu.Session, cpu_id: int, lin_addr: int, phy_addr: int):
    """Default callback for `clflush`

    The callback is called each time the CLFLUSH instruction is executed.
    """
    logging.debug(f"clflush_cb({sess=}, {cpu_id=}, {lin_addr=:#x}, {phy_addr=:#x})")


def cnear_branch_not_taken_cb(
    sess: bochscpu.Session, cpu_id: int, branch_ip: int, new_ip: int
):
    """Default callback for `cnear_branch_not_taken`

    The  callback  is  called  each time, when currently executed instruction is a
    conditional near branch and it is not taken.
    """
    logging.debug(
        f"cnear_branch_not_taken_cb({sess=}, {cpu_id=}, {branch_ip=:#x}, {new_ip=:#x})"
    )


def cnear_branch_taken_cb(
    sess: bochscpu.Session, cpu_id: int, branch_ip: int, new_ip: int
):
    """Default callback for `cnear_branch_taken`

    The  callback  is  called  each time, when currently executed instruction is a
    conditional near branch and it is taken.
    """
    logging.debug(
        f"cnear_branch_taken_cb({sess=}, {cpu_id=}, {branch_ip=:#x}, {new_ip=:#x})"
    )


def far_branch_cb(
    sess: bochscpu.Session,
    cpu_id: int,
    what: int,
    prev_cs: int,
    prev_ip: int,
    new_cs: int,
    new_ip: int,
):
    """Default callback for `far_branch`

    The  callback  is  called each time, when currently executed instruction is an
    unconditional far branch (always taken).
    """
    whatwhat = bochscpu.InstructionType(what)
    logging.debug(
        f"far_branch_cb({sess=}, {cpu_id=}, {whatwhat}, {prev_cs=:#x}, {prev_ip=:#x}, {new_cs=:#x}, {new_ip=:#x})"
    )


def hlt_cb(sess: bochscpu.Session, cpu_id: int):
    """Default callback for `hlt`

    The  callback  is called  each time,  when Bochs' emulated  CPU enters HALT or
    SHUTDOWN state.
    """
    logging.debug(f"hlt_cb({sess=}, {cpu_id=})")


def hw_interrupt_cb(sess: bochscpu.Session, cpu_id: int, vector: int, cs: int, ip: int):
    """Default callback for `hw_interrupt`

    The  callback  is  called  each time, when Bochs simulator executes a hardware
    interrupt.
    """
    logging.debug(f"hw_interrupt_cb({sess=}, {cpu_id=}, {vector=}, {cs=}, {ip=:#x})")


def inp_cb(sess: bochscpu.Session, cpu_id: int, len: int):
    """Default callback for `inp`

    These callback functions are a feedback from various system devices.
    """
    logging.debug(f"inp_cb({sess=}, {cpu_id=}, {len=})")


def inp2_cb(sess: bochscpu.Session, cpu_id: int, len: int, val: int):
    """Default callback for `inp2`

    These callback functions are a feedback from various system devices.
    """
    logging.debug(f"inp2_cb({sess=}, {cpu_id=}, {len=}, {val=})")


def interrupt_cb(sess: bochscpu.Session, cpu_id: int, int_num: int):
    """Default callback for `interrupt`

    The  callback  is called each time, when Bochs simulator executes an interrupt
    (software interrupt, hardware interrupt or an exception).
    """
    logging.debug(f"interrupt_cb({sess=}, {cpu_id=}, {int_num=})")


def lin_access_cb(
    sess: bochscpu.Session,
    cpu_id: int,
    lin: int,
    phy: int,
    len: int,
    memtype: int,
    rw: int,
):
    """Default callback for `lin_access`

    The  callback  is  called  each  time,  when Bochs simulator executes a linear
    memory  access.  Note  that  no  page split accesses will be generated because
    Bochs  splits  page split accesses to two different memory accesses during its
    execution  flow.  The  callback  also  will not be generated in case of direct
    physical memory access like page walks, SMM, VMM or SVM operations.
    """
    whatwhat = bochscpu.memory.AccessType(memtype)
    logging.debug(
        f"lin_access_cb(    {sess=}, {cpu_id=}, {lin=:#x}, {phy=:#x}, {len=}, {whatwhat=}, {rw=})"
    )


def mwait_cb(sess: bochscpu.Session, cpu_id: int, addr: int, len: int, flags: int):
    """Default callback for `mwait`

    The callback is called each time, when Bochs' emulated CPU enters to the MWAIT
    state.  The  callback  receives  monitored  memory  range and MWAIT flags as a
    parameters.
    """
    logging.debug(f"mwait_cb({sess=}, {cpu_id=}, {addr=:#x}, {len=}, {flags=})")


def opcode_cb(
    sess: bochscpu.Session,
    cpu_id: int,
    insn: int,
    opcode: int,
    len: int,
    is32: bool,
    is64: bool,
):
    """Default callback for `opcode`

    The  callback  is  called  each  time, when Bochs completes  to  decode  a new
    instruction.  Through  this callback function Bochs could provide an opcode of
    the instruction, opcode length and an execution mode (16/32/64).
    """
    logging.debug(
        f"opcode_cb({sess=}, {cpu_id=}, {insn=:#x}, {opcode=:#x}, {len=}, {is32=}, {is64=})"
    )


def outp_cb(sess: bochscpu.Session, cpu_id: int, len: int, val: int):
    """Default callback for `outp`

    These callback functions are a feedback from various system devices.
    """
    logging.debug(f"outp_cb({sess=}, {cpu_id=}, {len=}, {val=})")


def phy_access_cb(
    sess: bochscpu.Session, cpu_id: int, lin: int, phy: int, len: int, memtype: int
):
    """Default callback for `phy_access`

    The  callback  is called  each  time, when Bochs simulator executes a physical
    memory  access.  Physical  accesses include memory  accesses generated  by the
    CPU during  page walks, SMM, VMM or SVM  operations. Note that  no  page split
    accesses will be  generated because  Bochs splits  page split accesses  to two
    different memory accesses during its execution flow.
    """
    whatwhat = bochscpu.memory.AccessType(memtype)
    logging.debug(
        f"phy_access_cb({sess=}, {cpu_id=}, {lin=:#x}, {phy=:#x}, {len=}, {whatwhat})"
    )


def prefetch_hint_cb(
    sess: bochscpu.Session, cpu_id: int, what: int, seg: int, offset: int
):
    """Default callback for `prefetch_hint`

    The  callback  is  called  each time, when Bochs simulator executes a PREFETCH
    instruction.
    """
    whatwhat = bochscpu.PrefetchType(what)
    logging.debug(
        f"prefetch_hint_cb({sess=}, {cpu_id=}, {whatwhat}, {seg=:#x}, {offset=})"
    )


def repeat_iteration_cb(sess: bochscpu.Session, cpu_id: int, insn: int):
    """Default callback for `repeat_iteration`

    The  callback  is  called  each time, when Bochs simulator starts a new repeat
    iteration.
    """
    logging.debug(f"repeat_iteration_cb({sess=}, {cpu_id=}, {insn=:#x})")


def reset_cb(sess: bochscpu.Session, cpu_id: int, a2: int):
    """Default callback for `reset`

    The  callback  is called each time, when Bochs resets the CPU object. It would
    be  executed  once  at the start of simulation and each time that user presses
    RESET BUTTON on the simulator's control panel.
    """
    logging.debug(f"reset_cb({sess=}, {cpu_id=}, {a2=})")


def tlb_cntrl_cb(sess: bochscpu.Session, cpu_id: int, what: int, new_cr_value: int):
    """Default callback for `tlb_cntrl`

    The  callback  is  called each time, when Bochs simulator executes a tlb
    control instruction.
    """
    whatwhat = bochscpu.TlbControlType(what)
    logging.debug(f"tlb_cntrl_cb({sess=}, {cpu_id=}, {whatwhat}, {new_cr_value=:#x})")


def ucnear_branch_cb(
    sess: bochscpu.Session, cpu_id: int, what: int, branch_ip: int, new_branch_ip: int
):
    """Default callback for `ucnear_branch`

    The  callback  is  called each time, when currently executed instruction is an
    unconditional near branch (always taken).
    """
    whatwhat = bochscpu.InstructionType(what)
    logging.debug(
        f"ucnear_branch_cb({sess=}, {cpu_id=}, {whatwhat}, {branch_ip=:#x}, {new_branch_ip=:#x})"
    )


def vmexit_cb(sess: bochscpu.Session, cpu_id: int, reason: int, qualification: int):
    """Default callback for `vmexit`

    This callback is called right before Bochs executes a VMEXIT.
    """
    logging.debug(f"vmexit_cb({sess=}, {cpu_id=}, {reason=}, {qualification=})")


def wrmsr_cb(sess: bochscpu.Session, cpu_id: int, msr: int, value: int):
    """Default callback for `wrmsr`

    This callback is called each time when WRMSR instruction is executed.
    MSR number and written value passed as parameters to the callback function.
    """
    logging.debug(f"wrmsr_cb({sess=}, {cpu_id=}, {msr=:#x}, {value=})")


def install_default_callbacks(hook: bochscpu.Hook):
    """Install all default callbacks to the given hook.

    Args:
        hook (bochscpu.Hook): the hook to populate. Set callbacks will be replaced.
    """
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
    hook.inp2 = inp2_cb
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
