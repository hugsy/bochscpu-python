#
# This snippet does nothing, but can be used as a template for quickly build stuff from bochscpu
#
import logging

import bochscpu
import bochscpu.cpu
import bochscpu.memory
import bochscpu.utils


#
# Callbacks
#
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


#
# All the other callback prototypes - see `instrumentation.txt`
#
def cache_cntrl_cb(sess: bochscpu.Session, a1: int, a2: int):
    pass


def clflush_cb(sess: bochscpu.Session, a1: int, a2: int, a3: int):
    pass


def cnear_branch_not_taken_cb(sess: bochscpu.Session, a1: int, a2: int, a3: int):
    pass


def cnear_branch_taken_cb(sess: bochscpu.Session, a1: int, a2: int, a3: int):
    pass


def far_branch_cb(
    sess: bochscpu.Session, a1: int, a2: int, a3: int, a4: int, a5: int, a6: int
):
    pass


def hlt_cb(sess: bochscpu.Session, a1: int):
    pass


def hw_interrupt_cb(sess: bochscpu.Session, a1: int, a2: int, a3: int, a4: int):
    pass


def inp_cb(sess: bochscpu.Session, a1: int, a2: int):
    pass


def inp2_cb(sess: bochscpu.Session, a1: int, a2: int, a3: int):
    pass


def interrupt_cb(sess: bochscpu.Session, a1: int, a2: int):
    pass


def lin_access_cb(
    sess: bochscpu.Session, a1: int, a2: int, a3: int, a4: int, a5: int, a6: int
):
    pass


def mwait_cb(sess: bochscpu.Session, a1: int, a2: int, a3: int, a4: int):
    pass


def opcode_cb(
    sess: bochscpu.Session, a1: int, a2: int, a3: int, a4: int, a5: bool, a6: bool
):
    pass


def outp_cb(sess: bochscpu.Session, a1: int, a2: int, a3: int):
    pass


def phy_access_cb(sess: bochscpu.Session, a1: int, a2: int, a3: int, a4: int, a5: int):
    pass


def prefetch_hint_cb(sess: bochscpu.Session, a1: int, a2: int, a3: int, a4: int):
    pass


def repeat_iteration_cb(sess: bochscpu.Session, a1: int, a2: int):
    pass


def reset_cb(sess: bochscpu.Session, a1: int, a2: int):
    pass


def tlb_cntrl_cb(sess: bochscpu.Session, a1: int, a2: int, a3: int):
    pass


def ucnear_branch_cb(sess: bochscpu.Session, a1: int, a2: int, a3: int, a4: int):
    pass


def vmexit_cb(sess: bochscpu.Session, a1: int, a2: int, a3: int):
    pass


def wrmsr_cb(sess: bochscpu.Session, a1: int, a2: int, a3: int):
    pass


def emulate():
    #
    # Allocate a page on host, expose it to bochs, and fill it up
    #
    code_hva = bochscpu.memory.allocate_host_page()
    code_gpa = 0x0000_7000
    bochscpu.memory.page_insert(code_gpa, code_hva)
    bochscpu.memory.phy_write(code_gpa, b"\xcc" * bochscpu.memory.page_size())

    #
    # Create a session. A session **MUST** have at least a callback pointing to a custom
    # page fault handler
    #
    sess = bochscpu.Session()
    sess.missing_page_handler = missing_page_cb

    #
    # Create a CPU state and assign it to the session. The different x86 modes can be set
    # thanks to helpers located in `bochscpu.cpu.set_XXXX_mode` where XXXX can be:
    # - real
    # - virtual8086
    # - protected
    # - long
    #
    state = bochscpu.State()
    bochscpu.cpu.set_real_mode(state)

    state.rip = code_gpa
    state.rsp = code_gpa + 0x0800
    sess.cpu.state = state

    #
    # Defines hook: a hook is one specific set of callbacks. Many hooks can be created, and
    # they are all chained together when running the code
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

    #
    # Create the hook chain
    #
    hooks = [
        hook,  # here we only have one but we can set many
    ]

    #
    # Start the emulation
    #
    sess.run(hooks)

    #
    # With the execution finished, you can read the final state of the CPU
    #
    final_state = sess.cpu.state
    print(f"RIP={final_state.rip:#x}")
    bochscpu.memory.release_host_page(code_hva)


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
    emulate()
    # Note: it is recommended to use an intermediary function like `emulate`
    # rather than emulating directly from `main`. Finishing main will result
    # in a process exit, prevent some object to be correctly cleaned which
    # may resulting in `nanobind` throwing exception on object deletions.
