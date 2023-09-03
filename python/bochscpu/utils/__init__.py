import struct

import bochscpu.memory
import bochscpu._bochscpu as _bochscpu

from . import cpu

PAGE_SIZE = bochscpu.memory.page_size()


def dump_registers(state: _bochscpu.State, include_kernel: bool = False):
    """Print registers for a given `State` in a WinDbg display type

    Args:
        state (_bochscpu.State): _description_
        include_kernel (bool): _description_
    """
    print(
        f"""
rax={state.rax:016x} rbx={state.rbx:016x} rcx={state.rcx:016x}
rdx={state.rdx:016x} rsi={state.rsi:016x} rdi={state.rdi:016x}
rip={state.rip:016x} rsp={state.rsp:016x} rbp={state.rbp:016x}
 r8={ state.r8:016x}  r9={ state.r9:016x} r10={state.r10:016x}
r11={state.r11:016x} r12={state.r12:016x} r13={state.r13:016x}
r14={state.r14:016x} r15={state.r15:016x} efl={state.rflags:016x}
cs={int(state.cs):04x}  ss={int(state.ss):04x}  ds={int(state.ds):04x}  es={int(state.es):04x}  fs={int(state.fs):04x}  gs={int(state.gs):04x}
"""
    )

    if not include_kernel:
        return

    print(
        f"""
cr0={state.cr0:016x}  cr2={state.cr2:016x}  cr3={state.cr3:016x}  cr4={state.cr4:016x}
dr0={state.dr0:016x}  dr1={state.dr1:016x}  dr2={state.dr2:016x}  dr3={state.dr3:016x}
dr6={state.dr6:016x}  dr7={state.dr7:016x} xcr0={state.xcr0:016x} efer={state.efer:016x}
"""
    )
    return


def dump_page_table(pml4: int):
    """Dump a Page Table from its PML4

    Args:
        pml4 (int): _description_
    """

    def __dump_page_table(addr: int, level: int = 0):
        level_str = ("PML", "PDPT", "PD", "PT")
        if level == 4:
            data = bytes(bochscpu.memory.phy_read(addr, 8))
            entry = struct.unpack("<Q", data[:8])[0] & ~0xFFF
            print(f"{' '*level} {entry:#x}")
            return

        print(f"Dumping {level_str[level]}Es @ {addr:#x}")

        for i in range(0, PAGE_SIZE, 8):
            data = bytes(bochscpu.memory.phy_read(addr + i, 8))
            entry = struct.unpack("<Q", data[:8])[0]
            flags = entry & 0xFFF
            entry = entry & ~0xFFF
            if entry == 0:
                continue
            print(f"{' '*level} #{i//8} - {hex(entry)}|{flags=:#x}")
            __dump_page_table(entry, level + 1)
        return

    __dump_page_table(pml4, 0)
