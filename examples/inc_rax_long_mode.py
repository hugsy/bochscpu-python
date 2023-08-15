import struct

from typing import Any

import ctypes
import time
import bochscpu

DEBUG = True

executed_instruction_nb: int = 0


def dbg(x):
    if DEBUG:
        print(f"[Py] {x}")


def VirtualAlloc(sz: int = bochscpu.memory.PageSize(), perm: str = "rwx"):
    MEM_COMMIT = 0x1000
    MEM_RESERVE = 0x2000
    PAGE_NOACCESS = 0x01
    PAGE_READONLY = 0x02
    PAGE_READWRITE = 0x04
    PAGE_EXECUTE_READWRITE = 0x40
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    VirtualAlloc = kernel32.VirtualAlloc
    VirtualAlloc.argtypes = [
        ctypes.c_void_p,
        ctypes.c_size_t,
        ctypes.c_ulong,
        ctypes.c_ulong,
    ]
    VirtualAlloc.restype = ctypes.c_void_p
    flags = PAGE_NOACCESS
    match perm:
        case "ro":
            flags = PAGE_READONLY
        case "rw":
            flags = PAGE_READWRITE
        case "rwx":
            flags = PAGE_EXECUTE_READWRITE
        case _:
            raise ValueError

    return VirtualAlloc(None, sz, MEM_COMMIT | MEM_RESERVE, flags)


def dump_page_table(addr: int, level: int = 0):
    level_str = ("PML", "PDPT", "PD", "PT")
    if level == 4:
        data = bytes(bochscpu.bochscpu_mem_phy_read(addr, 8))
        entry = struct.unpack("<Q", data[:8])[0] & ~0xFFF
        print(f"{' '*level} {entry:#x}")
        return

    print(f"Dumping {level_str[level]} @ {addr:#x}")

    for i in range(0, bochscpu.memory.PageSize(), 8):
        data = bytes(bochscpu.bochscpu_mem_phy_read(addr + i, 8))
        entry = struct.unpack("<Q", data[:8])[0]
        flags = entry & 0xFFF
        entry = entry & ~0xFFF
        if entry == 0:
            continue
        print(f"{' '*level} #{i//8} - {hex(entry)}|{flags=:#x}")
        dump_page_table(entry, level + 1)


def missing_page_cb(gpa: int) -> None:
    raise Exception(f"missing_page_cb({gpa=:#x})")


def exception_cb(ctx: Any, cpu_id: int, vector: int, error_code: int):
    dbg(f"received `exception({vector=:d}, {error_code=:d})` from cpu#{cpu_id}")
    cpu = bochscpu.bochscpu_cpu_from(cpu_id)
    bochscpu.bochscpu_cpu_stop(cpu)


def after_execution_cb(ctx: Any, cpu_id: int, insn: int):
    global executed_instruction_nb
    executed_instruction_nb += 1


def emulate(code: bytearray):
    CODE = 0
    RW = 1

    #
    # Setup the PF handler very early to let Python handle it, rather than rust panicking
    #
    dbg("setting pf handler")
    bochscpu.bochscpu_mem_missing_page(missing_page_cb)

    #
    # Setup control registers to enable PG/PE and long mode
    #
    cr0 = bochscpu.cpu.ControlRegister()
    cr0.PG = True
    cr0.AM = True
    cr0.WP = True
    cr0.NE = True
    cr0.ET = True
    cr0.PE = True
    dbg(f"{int(cr0)=:#016x}")

    cr4 = bochscpu.cpu.ControlRegister()
    cr4.PAE = True  # required for long mode
    dbg(f"{int(cr4)=:#016x}")

    #
    # Manually craft the guest virtual & physical memory layout into a pagetable
    # Once done bind the resulting GPAs it to bochs
    #
    shellcode_hva = VirtualAlloc()
    shellcode_gva = 0x0400_0000
    shellcode_gpa = 0x1400_0000
    dbg(f"inserting {shellcode_gva=:#x} -> {shellcode_gpa=:#x} ->  {shellcode_hva=:#x}")
    bochscpu.bochscpu_mem_page_insert(shellcode_gpa, shellcode_hva)

    stack_hva = VirtualAlloc(perm="rw")
    stack_gva = 0x0401_0000
    stack_gpa = 0x1401_0000
    dbg(f"inserting {stack_gva=:#x} -> {stack_gpa=:#x} -> {stack_hva=:#x}")
    bochscpu.bochscpu_mem_page_insert(stack_gpa, stack_hva)

    pt = bochscpu.memory.PageMapLevel4Table()
    pt.Insert(stack_gva, stack_gpa, RW)
    pt.Insert(shellcode_gva, shellcode_gpa, CODE)

    assert pt.Translate(stack_gva) == stack_gpa
    assert pt.Translate(shellcode_gva) == shellcode_gpa

    pml4 = 0x10_0000
    layout = pt.Commit(pml4)

    for hva, gpa in layout:
        bochscpu.bochscpu_mem_page_insert(gpa, hva)
        evaled_gpa = bochscpu.bochscpu_mem_phy_translate(gpa)
        assert evaled_gpa == hva, f"{evaled_gpa=:#x} == {hva=:#x}"

    evaled_gpa = bochscpu.bochscpu_mem_virt_translate(pml4, shellcode_gva)
    assert evaled_gpa == shellcode_gpa, f"{evaled_gpa=:#x} != {shellcode_gpa=:#x}"
    evaled_gpa = bochscpu.bochscpu_mem_virt_translate(pml4, stack_gva)
    assert evaled_gpa == stack_gpa, f"{evaled_gpa=:#x} != {stack_gpa=:#x}"

    # dump_page_table(pml4)

    dbg(f"copy code to {shellcode_gva=:#x}")
    assert bochscpu.bochscpu_mem_virt_write(pml4, shellcode_gva, bytes(code))
    dbg(f"copied to {shellcode_gva=:#x}, testing...")
    data = bochscpu.bochscpu_mem_virt_read(pml4, shellcode_gva, len(code))
    assert data
    assert bytes(data) == bytes(code), f"{bytes(data).hex()} != {bytes(code).hex()}"
    dbg("success")

    #
    # Create a state and load it into a new CPU
    #
    cpu = bochscpu.bochscpu_cpu_new(0)
    dbg("created cpu#0")

    state = bochscpu.State()
    state.rax = 0x10
    state.rsp = stack_gva
    state.rip = shellcode_gva
    state.cr0 = int(cr0)
    state.cr3 = pml4
    state.cr4 = int(cr4)
    state.efer = 0xD01
    cs = bochscpu.Segment()
    cs.present = True
    cs.selector = 0x33
    cs.base = 0
    cs.limit = 0xFFFF_FFFF
    cs.attr = 0x22FB
    state.cs = cs
    ds = bochscpu.Segment()
    ds.present = True
    ds.selector = 0x2B
    ds.base = 0
    ds.limit = 0xFFFF_FFFF
    ds.attr = 0xCF3
    state.ds = ds
    state.ss = ds
    state.es = ds
    state.fs = ds
    state.gs = ds
    bochscpu.bochscpu_cpu_set_state(cpu, state)
    dbg("loaded state for cpu#0")

    hooks = []
    hook = bochscpu.Hook()
    hook.exception = exception_cb
    hook.after_execution = after_execution_cb
    hooks.append(hook)
    dbg("hooks ok")

    dbg("starting the vm...")
    t1 = time.time()
    bochscpu.bochscpu_cpu_run(cpu, hooks)
    t2 = time.time()
    dbg(
        f"vm stopped, execution: {executed_instruction_nb} insns in {float((t2-t1)*1000.0)}ms"
    )

    dbg("reading new state")
    new_state = bochscpu.State()
    bochscpu.bochscpu_cpu_state(cpu, new_state)
    dbg(f"{state.rax=:#x} vs {new_state.rax=:#x}")
    bochscpu.bochscpu_cpu_delete(cpu)

    assert state.rax + 8 == new_state.rax
    return


if __name__ == "__main__":
    emulate(
        bytearray(
            # fmt: off
            [
                0x48, 0xff, 0xc0,  # inc rax
                0x48, 0xff, 0xc0,  # inc rax
                0x48, 0xff, 0xc0,  # inc rax
                0x48, 0xff, 0xc0,  # inc rax

                0x48, 0xff, 0xc0,  # inc rax
                0x48, 0xff, 0xc0,  # inc rax
                0x48, 0xff, 0xc0,  # inc rax
                0x48, 0xff, 0xc0,  # inc rax

                0xf4               # hlt
            ]
            # fmt: on
        )
    )
