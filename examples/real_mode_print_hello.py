import logging
import os

import keystone
import bochscpu
import bochscpu.cpu
import bochscpu.memory


def hexdump(
    source: bytes, length: int = 0x10, separator: str = ".", base: int = 0x00
) -> str:
    result = []
    align = 0x8 * 2 + 2

    for i in range(0, len(source), length):
        chunk = bytearray(source[i : i + length])
        hexa = " ".join(map(lambda x: f"{x:02X}", chunk))
        text = "".join([chr(b) if 0x20 <= b < 0x7F else separator for b in chunk])
        result.append(f"{base + i:#0{align}x}   {hexa:<{3 * length}}    {text}")
    return os.linesep.join(result)


def missing_page_cb(gpa: int):
    raise Exception(f"missing_page_cb({gpa=:#x})")


def after_execution_cb(sess: bochscpu.Session, cpu_id: int, insn: int):
    logging.info(f"[CPU#{cpu_id}] {insn=}")


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
mov al, 0x41
int 0x16
hlt
"""
    code, _ = ks.asm(code_str)
    assert isinstance(code, list)
    code = bytes(code)
    logging.debug(f"Compiled {len(code)} bytes")
    code = code.ljust(510, b"\x00") + b"\x55\xaa"

    # print(hexdump(code))

    #
    # Expose the code to bochs
    #
    hva = bochscpu.memory.allocate_host_page()
    gpa = 0x0000_7000
    bochscpu.memory.page_insert(gpa, hva)
    bochscpu.memory.phy_write(gpa, code)

    #
    # Create the VM with the desired callbacks
    #
    sess = bochscpu.Session()
    sess.missing_page_handler = missing_page_cb

    state = bochscpu.State()
    state.cr0 = 0
    state.cr4 = 0
    state.rsp = gpa + bochscpu.memory.page_size() // 2
    state.rip = gpa
    sess.cpu.state = state

    h = bochscpu.Hook()
    h.exception = exception_cb
    h.after_execution = after_execution_cb

    sess.run(
        [
            h,
        ]
    )

    #
    # Cleanup
    #
    bochscpu.memory.release_host_page(hva)
