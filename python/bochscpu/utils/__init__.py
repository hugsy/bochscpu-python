import struct
from typing import Optional

import bochscpu.cpu
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

    gprs: dict[str, tuple[Optional[str], Optional[str], str]] = {
        # keyname: (real, protected, long)
        "rax": ("ax", "eax", "rax"),
        "rbx": ("bx", "ebx", "rbx"),
        "rdx": ("cx", "ecx", "rcx"),
        "rdx": ("dx", "edx", "rdx"),
        "rsi": ("si", "esi", "rsi"),
        "rdi": ("di", "edi", "rdi"),
        "rbp": ("bp", "ebp", "rbp"),
        "rsp": ("sp", "esp", "rsp"),
        "rip": ("ip", "eip", "rip"),
        "r8": (None, None, " r8"),
        "r9": (None, None, " r9"),
        "r10": (None, None, "r10"),
        "r11": (None, None, "r11"),
        "r12": (None, None, "r12"),
        "r13": (None, None, "r13"),
        "r14": (None, None, "r14"),
        "r15": (None, None, "r15"),
    }

    if bochscpu.cpu.is_real_mode(state):
        idx = 0
        fmt = 8
    elif bochscpu.cpu.is_protected_mode(state):
        idx = 1
        fmt = 8
    elif bochscpu.cpu.is_long_mode(state):
        idx = 2
        fmt = 16
    else:
        raise Exception("invalid state")

    i = 0
    max_regs_per_line = 3
    for reg, names in gprs.items():
        if i % max_regs_per_line == 0:
            print("")
        name = names[idx]
        if not name:
            continue
        value = getattr(state, reg)
        print(f"{name}={value:0{fmt}x}", end=" ")
        i += 1

    print(
        f"""
efl={state.rflags:08x} {str(bochscpu.cpu.FlagRegister(state.rflags))}
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
