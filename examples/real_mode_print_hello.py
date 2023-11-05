import logging
import os

import keystone
import bochscpu
import bochscpu.cpu
import bochscpu.memory
import bochscpu.utils


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
    logging.info(f"[CPU#{cpu_id}] before PC={sess.cpu.rip:#x}")


def after_execution_cb(sess: bochscpu.Session, cpu_id: int, _: int):
    logging.info(f"[CPU#{cpu_id}] after PC={sess.cpu.rip:#x}")


def phy_access_cb(sess, cpu_id, a2, a3, a4, a5):
    logging.debug(f"[CPU#{cpu_id}] {a2=:#x}")


def reset_cb(sess, a1, a2):
    logging.debug(f"{a1=:} {a2=:}")


def interrupt_cb(sess, a1, a2):
    logging.debug(f"{a1=:} {a2=:}")


def hw_interrupt_cb(sess, a1, a2, a3, a4):
    logging.debug(f"{a1=:} {a2=:}")


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


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

    #
    # Use Keystone to compile the assembly
    #
    ks = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_16)
    code_str = """
loop:
jmp loop

hlt
"""
    code, _ = ks.asm(code_str)
    assert isinstance(code, list)
    code = bytes(code)
    logging.debug(f"Compiled {len(code)} bytes")
    code = code.ljust(510, b"\x00") + b"\x55\xaa"

    # print(hexdump(code))

    #
    # Create the code page
    #
    code_hva = bochscpu.memory.allocate_host_page()
    code_gpa = 0x000_7000
    bochscpu.memory.page_insert(code_gpa, code_hva)
    bochscpu.memory.phy_write(code_gpa + 0xC00, code)

    # _cs = bochscpu.Segment()
    # _cs.base = 0
    # _cs.limit = 0x0000_0FFF
    # _cs.selector = 0x0000
    # cs_attr = bochscpu.cpu.SegmentFlags()
    # cs_attr.P = True
    # cs_attr.E = True
    # cs_attr.DB = False
    # cs_attr.G = False
    # _cs.attr = int(cs_attr)
    # _cs.present = True

    # _ds = bochscpu.Segment()
    # _ds.base = 0
    # _ds.limit = 0x0000_0FFF
    # _ds.selector = 0x0000
    # ds_attr = bochscpu.cpu.SegmentFlags()
    # ds_attr.P = True
    # ds_attr.E = False
    # ds_attr.DB = False
    # ds_attr.G = False
    # _ds.attr = int(ds_attr)
    # _ds.present = True

    # _ss = bochscpu.Segment()
    # _ss.present = True
    # _ss.base = 0
    # _ss.selector = 0x0000
    # _ss.limit = 0x0000_7FFF
    # ss_attr = bochscpu.cpu.SegmentFlags()
    # ss_attr.D = True
    # ss_attr.W = True
    # ss_attr.G = False
    # _ss.attr = int(ss_attr)

    #
    # Create the VM with the desired callbacks
    #
    sess = bochscpu.Session()
    sess.missing_page_handler = missing_page_cb

    state = bochscpu.State()
    bochscpu.cpu.set_real_mode(state)

    #
    # Assign segment to the state, CS and SS are always required
    #
    # state.cs = _cs
    # state.ss = _ss

    state.rsp = 0x7000
    state.rip = 0x7C00

    # bochscpu.utils.dump_registers(state)

    sess.cpu.state = state

    h = bochscpu.Hook()
    h.exception = exception_cb
    h.before_execution = before_execution_cb
    h.after_execution = after_execution_cb
    h.phy_access = phy_access_cb
    h.reset = reset_cb
    h.interrupt = interrupt_cb
    h.hw_interrupt = hw_interrupt_cb

    sess.run(
        [
            h,
        ]
    )

    #
    # Cleanup
    #
    bochscpu.memory.release_host_page(code_hva)
