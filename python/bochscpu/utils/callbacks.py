import logging

import bochscpu
import bochscpu.cpu


def missing_page_cb(gpa: int):
    """Edit this function to change the page fault behavior
    Args:
        gpa (int): the physical address of where the page fault occured
    """
    raise RuntimeError(f"missing_page_cb({gpa=:#x})")


def before_execution_cb(sess: bochscpu.Session, cpu_id: int, _: int):
    logging.debug(f"[CPU#{cpu_id}] before PC={sess.cpu.rip:#x}")


def after_execution_cb(sess: bochscpu.Session, cpu_id: int, _: int):
    logging.debug(f"[CPU#{cpu_id}] after PC={sess.cpu.rip:#x}")


def exception_cb(
    sess: bochscpu.Session,
    cpu_id: int,
    vector: int,
    error_code: int,
):
    v = bochscpu.cpu.ExceptionType(vector)
    match (vector, error_code):
        case _:
            logging.warning(f"cpu#{cpu_id} received exception({v}, {error_code=:d}) ")
    sess.stop()


def cache_cntrl_cb(sess: bochscpu.Session, cpu_id: int, what: int):
    """Default callback for `cache_cntrl`

    The  callback  is  called each time, when Bochs simulator executes a cache/tlb
    control instruction.
    """
    whatwhat = bochscpu.CacheControlType(what)
    logging.debug(f"cache_cntrl_cb({sess=}, {cpu_id=}, {whatwhat})")


def clflush_cb(sess: bochscpu.Session, cpu_id: int, lin_addr: int, phy_addr: int):
    """Default callback for `clflush`"""
    logging.debug(f"clflush_cb({sess=}, {cpu_id=}, {lin_addr=:#x}, {phy_addr=:#x})")


def cnear_branch_not_taken_cb(
    sess: bochscpu.Session, cpu_id: int, branch_ip: int, new_ip: int
):
    """Default callback for `cnear_branch_not_taken`"""
    logging.debug(
        f"cnear_branch_not_taken_cb({sess=}, {cpu_id=}, {branch_ip=:#x}, {new_ip=:#x})"
    )


def cnear_branch_taken_cb(
    sess: bochscpu.Session, cpu_id: int, branch_ip: int, new_ip: int
):
    """Default callback for `cnear_branch_taken`"""
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
    """Default callback for `far_branch`"""
    logging.debug(
        f"far_branch_cb({sess=}, {cpu_id=}, {what=:#x}, {prev_cs=:#x}, {prev_ip=:#x}, {new_cs=:#x}, {new_ip=:#x})"
    )


def hlt_cb(sess: bochscpu.Session, cpu_id: int):
    """Default callback for `hlt`"""
    logging.debug(f"hlt_cb({sess=}, {cpu_id=})")


def hw_interrupt_cb(sess: bochscpu.Session, cpu_id: int, vector: int, cs: int, ip: int):
    """Default callback for `hw_interrupt`"""
    logging.debug(f"hw_interrupt_cb({sess=}, {cpu_id=}, {vector=}, {cs=}, {ip=:#x})")


def inp_cb(sess: bochscpu.Session, cpu_id: int, len: int):
    """Default callback for `inp`"""
    logging.debug(f"inp_cb({sess=}, {cpu_id=}, {len=})")


def inp2_cb(sess: bochscpu.Session, cpu_id: int, len: int, val: int):
    """Default callback for `inp2`"""
    logging.debug(f"inp2_cb({sess=}, {cpu_id=}, {len=}, {val=})")


def interrupt_cb(sess: bochscpu.Session, cpu_id: int, int_num: int):
    """Default callback for `interrupt`"""
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
    """Default callback for `lin_access`"""
    logging.debug(
        f"lin_access_cb(    {sess=}, {cpu_id=}, {lin=:#x}, {phy=:#x}, {len=}, {memtype=}, {rw=})"
    )


def mwait_cb(sess: bochscpu.Session, cpu_id: int, addr: int, len: int, flags: int):
    """Default callback for `mwait`"""
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
    """Default callback for `opcode`"""
    logging.debug(
        f"opcode_cb({sess=}, {cpu_id=}, {insn=:#x}, {opcode=:#x}, {len=}, {is32=}, {is64=})"
    )


def outp_cb(sess: bochscpu.Session, cpu_id: int, len: int, val: int):
    """Default callback for `outp`"""
    logging.debug(f"outp_cb({sess=}, {cpu_id=}, {len=}, {val=})")


def phy_access_cb(
    sess: bochscpu.Session, cpu_id: int, lin: int, phy: int, len: int, rw: int
):
    """Default callback for `phy_access`"""
    logging.debug(
        f"phy_access_cb({sess=}, {cpu_id=}, {lin=:#x}, {phy=:#x}, {len=}, {rw=})"
    )


def prefetch_hint_cb(
    sess: bochscpu.Session, cpu_id: int, what: int, seg: int, offset: int
):
    """Default callback for `prefetch_hint`"""
    whatwhat = bochscpu.PrefetchType(what)
    logging.debug(
        f"prefetch_hint_cb({sess=}, {cpu_id=}, {whatwhat}, {seg=:#x}, {offset=})"
    )


def repeat_iteration_cb(sess: bochscpu.Session, cpu_id: int, insn: int):
    """Default callback for `repeat_iteration`"""
    logging.debug(f"repeat_iteration_cb({sess=}, {cpu_id=}, {insn=:#x})")


def reset_cb(sess: bochscpu.Session, cpu_id: int, a2: int):
    """Default callback for `reset`"""
    logging.debug(f"reset_cb({sess=}, {cpu_id=}, {a2=})")


def tlb_cntrl_cb(sess: bochscpu.Session, cpu_id: int, what: int, new_cr_value: int):
    """Default callback for `tlb_cntrl`"""
    whatwhat = bochscpu.TlbControlType(what)
    logging.debug(f"tlb_cntrl_cb({sess=}, {cpu_id=}, {whatwhat}, {new_cr_value=:#x})")


def ucnear_branch_cb(
    sess: bochscpu.Session, cpu_id: int, what: int, branch_ip: int, new_branch_ip: int
):
    """Default callback for `ucnear_branch`"""
    logging.debug(
        f"ucnear_branch_cb({sess=}, {cpu_id=}, {what=}, {branch_ip=:#x}, {new_branch_ip=:#x})"
    )


def vmexit_cb(sess: bochscpu.Session, cpu_id: int, reason: int, qualification: int):
    """Default callback for `vmexit`"""
    logging.debug(f"vmexit_cb({sess=}, {cpu_id=}, {reason=}, {qualification=})")


def wrmsr_cb(sess: bochscpu.Session, cpu_id: int, msr: int, value: int):
    """Default callback for `wrmsr`"""
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
