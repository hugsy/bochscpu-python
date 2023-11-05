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


def phy_access_cb(sess: bochscpu.Session, cpu_id, a2, a3, a4, a5):
    logging.debug(f"[CPU#{cpu_id}] {a2=:#x}")


def reset_cb(sess: bochscpu.Session, a1, a2):
    logging.debug(f"{a1=:} {a2=:}")


def interrupt_cb(sess: bochscpu.Session, a1, a2):
    logging.debug(f"{a1=:} {a2=:}")


def hw_interrupt_cb(sess: bochscpu.Session, a1, a2, a3, a4):
    logging.debug(f"{a1=:} {a2=:} {a3=:} {a4=:} ")


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


def run():
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
    # Define one (or several) chains of callbacks and bind them to the session
    #
    hook = bochscpu.Hook()
    hook.exception = exception_cb
    hook.before_execution = before_execution_cb
    hook.after_execution = after_execution_cb
    hook.phy_access = phy_access_cb
    hook.reset = reset_cb
    hook.interrupt = interrupt_cb
    hook.hw_interrupt = hw_interrupt_cb

    #
    # Let it go
    #
    sess.run(
        [
            hook,
        ]
    )

    #
    # With the execution finished, you can read the final state of the CPU
    #
    final_state = sess.cpu.state
    print(f"RIP={final_state.rip:#x}")
    bochscpu.memory.release_host_page(code_hva)


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
    run()
