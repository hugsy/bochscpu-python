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
mov ah, 0xe
mov al, 'A'
int 0x10
hlt
"""
    code, _ = ks.asm(code_str)
    assert isinstance(code, list)
    code = bytes(code)
    logging.debug(f"Compiled {len(code)} bytes")
    code = code.ljust(510, b"\x00") + b"\x55\xaa"

    print(hexdump(code))

    #
    # Create the code page
    #
    code_hva = bochscpu.memory.allocate_host_page()
    code_gpa = 0x0000_7000
    bochscpu.memory.page_insert(code_gpa, code_hva)
    bochscpu.memory.phy_write(code_gpa, code)

    _cs = bochscpu.Segment()
    _cs.base = code_gpa + 0x800
    _cs.limit = 0x0000_0FFF
    _cs.selector = 0x0010
    cs_attr = bochscpu.cpu.SegmentFlags()
    cs_attr.P = True
    cs_attr.E = True
    cs_attr.DB = False
    cs_attr.G = False
    _cs.attr = int(cs_attr)
    _cs.present = True

    _ss = bochscpu.Segment()
    _ss.present = True
    _ss.base = code_gpa
    _ss.selector = 0
    _ss.attr = 0
    _ss.limit = 0x0000_000F

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
    state.cs = _cs
    state.ss = _ss

    state.rsp = 0x0000
    state.rip = 0x0C00

    sess.cpu.state = state

    h = bochscpu.Hook()
    h.exception = exception_cb
    h.before_execution = before_execution_cb
    h.after_execution = after_execution_cb

    sess.run(
        [
            h,
        ]
    )

    #
    # Cleanup
    #
    bochscpu.memory.release_host_page(code_hva)
