import struct
import time

import capstone
import keystone

import bochscpu
import bochscpu.cpu
import bochscpu.memory
import bochscpu.utils


DEBUG = True
PAGE_SIZE = bochscpu.memory.page_size()


class Stats:
    insn_nb: int = 0
    mem_access: dict[bochscpu.memory.AccessType, int] = {
        bochscpu.memory.AccessType.Read: 0,
        bochscpu.memory.AccessType.Write: 0,
        bochscpu.memory.AccessType.Execute: 0,
    }


stats = Stats()


def dbg(x: str):
    if DEBUG:
        print(f"[Py] {x}")


def dump_page_table(addr: int, level: int = 0):
    level_str = ("PML", "PDPT", "PD", "PT")
    if level == 4:
        data = bytes(bochscpu.memory.phy_read(addr, 8))
        entry = struct.unpack("<Q", data[:8])[0] & ~0xFFF
        print(f"{' '*level} {entry:#x}")
        return

    print(f"Dumping {level_str[level]} @ {addr:#x}")

    for i in range(0, PAGE_SIZE, 8):
        data = bytes(bochscpu.memory.phy_read(addr + i, 8))
        entry = struct.unpack("<Q", data[:8])[0]
        flags = entry & 0xFFF
        entry = entry & ~0xFFF
        if entry == 0:
            continue
        print(f"{' '*level} #{i//8} - {hex(entry)}|{flags=:#x}")
        dump_page_table(entry, level + 1)


def missing_page_cb(gpa):
    raise Exception(f"missing_page_cb({gpa=:#x})")


def exception_cb(
    sess: bochscpu.Session,
    cpu_id: int,
    vector: bochscpu.cpu.ExceptionType,
    error_code: bochscpu.InstructionType,
):
    match (vector, error_code):
        case _:
            dbg(f"cpu#{cpu_id} received exception({vector=:d}, {error_code=:d}) ")
    sess.stop()


def lin_access_cb(
    sess: bochscpu.Session,
    cpu_id: int,
    lin: int,
    phy: int,
    len: int,
    rw: int,
    access: bochscpu.memory.AccessType,
):
    global stats
    # dbg(f"{lin=:#x} {phy=:#x} {len=:d} {rw=:d} {access=:d}")
    stats.mem_access[access] += 1


def after_execution_cb(sess: bochscpu.Session, cpu_id: int, insn: int):
    global stats
    stats.insn_nb += 1


def emulate(code: bytes):
    CODE = 0
    RW = 1

    #
    # Setup the PF handler very early to let Python handle it, rather than rust panicking
    #
    sess = bochscpu.Session()
    dbg(f"created session for cpu#{sess.cpu.id}")

    sess.missing_page_handler = missing_page_cb
    dbg("registered our own missing page handler")

    #
    # Manually craft the guest virtual & physical memory layout into a pagetable
    # Once done bind the resulting GPAs it to bochs
    #
    shellcode_hva = bochscpu.memory.allocate_host_page()
    shellcode_gva = 0x0000_0041_0000_0000
    shellcode_gpa = 0x0000_0000_1400_0000
    dbg(f"inserting {shellcode_gva=:#x} -> {shellcode_gpa=:#x} ->  {shellcode_hva=:#x}")
    bochscpu.memory.page_insert(shellcode_gpa, shellcode_hva)

    stack_hva = bochscpu.memory.allocate_host_page()
    stack_gva = 0x0401_0000_0000
    stack_gpa = 0x1401_0000
    dbg(f"inserting {stack_gva=:#x} -> {stack_gpa=:#x} -> {stack_hva=:#x}")
    bochscpu.memory.page_insert(stack_gpa, stack_hva)

    pt = bochscpu.memory.PageMapLevel4Table()
    pt.insert(stack_gva, stack_gpa, RW)
    pt.insert(shellcode_gva, shellcode_gpa, CODE)

    assert pt.translate(stack_gva) == stack_gpa
    assert pt.translate(shellcode_gva) == shellcode_gpa

    pml4 = 0x10_0000
    layout = pt.commit(pml4)

    for hva, gpa in layout:
        bochscpu.memory.page_insert(gpa, hva)
        evaled_gpa = bochscpu.memory.phy_translate(gpa)
        assert evaled_gpa == hva, f"{evaled_gpa=:#x} == {hva=:#x}"

    evaled_gpa = bochscpu.memory.virt_translate(pml4, shellcode_gva)
    assert evaled_gpa == shellcode_gpa, f"{evaled_gpa=:#x} != {shellcode_gpa=:#x}"
    evaled_gpa = bochscpu.memory.virt_translate(pml4, stack_gva)
    assert evaled_gpa == stack_gpa, f"{evaled_gpa=:#x} != {stack_gpa=:#x}"

    # dump_page_table(pml4)

    dbg(f"copy code to {shellcode_gva=:#x}")
    assert bochscpu.memory.virt_write(pml4, shellcode_gva, bytes(code))
    dbg(f"copied to {shellcode_gva=:#x}, testing...")
    data = bochscpu.memory.virt_read(pml4, shellcode_gva, len(code))
    assert data
    assert bytes(data) == bytes(code), f"{bytes(data).hex()} != {bytes(code).hex()}"
    dbg("success")

    #
    # Create a state and load it into a new CPU
    #
    state = bochscpu.State()

    #
    # Setup control registers to enable PG/PE and long mode
    #
    bochscpu.cpu.set_long_mode(state)

    #
    # Initialize CR3 with PML4 base.
    #
    state.cr3 = pml4

    #
    # Set the other registers
    #
    state.rsp = stack_gva + PAGE_SIZE // 2
    state.rip = shellcode_gva

    #
    # Set the selectors
    #
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

    #
    # Assign the state
    #
    sess.cpu.state = state
    dbg("loaded state for cpu#0")
    dbg("dumping start state")
    bochscpu.utils.dump_registers(sess.cpu.state)

    hook = bochscpu.Hook()
    hook.exception = exception_cb
    hook.after_execution = after_execution_cb
    hook.lin_access = lin_access_cb
    dbg("hook setup ok")

    dbg("starting the vm...")
    t1 = time.time_ns()
    sess.run(
        [
            hook,
        ]
    )
    t2 = time.time_ns()
    dbg(
        f"vm stopped, execution: {stats.insn_nb} insns in {t2-t1}ns (~{int(stats.insn_nb // ((t2-t1)/1_000_000_000))}) insn/s"
    )
    dbg(
        f"mem accesses: read={stats.mem_access[bochscpu.memory.AccessType.Read]} "
        f"write={stats.mem_access[bochscpu.memory.AccessType.Write]} "
        f"execute={stats.mem_access[bochscpu.memory.AccessType.Execute]}"
    )

    if stats.insn_nb < len(INSNS):
        dbg(f"last insn executed: {INSNS[stats.insn_nb]}")
    if stats.insn_nb - 1 < len(INSNS):
        dbg(f"next insn: {INSNS[stats.insn_nb+1]}")

    dbg("reading new state")
    new_state = sess.cpu.state
    dbg("dumping final state")
    bochscpu.utils.dump_registers(new_state)

    bochscpu.memory.release_host_page(stack_hva)
    bochscpu.memory.release_host_page(shellcode_hva)
    return


if __name__ == "__main__":
    # from https://github.com/yrp604/bochscpu-bench/tree/master/asm
    ks = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
    fib = """
_start:
    push 0
    push 0
    push 1

loop:
    pop rax
    pop rbx
    pop rcx

    mov rdx, rax
    add rax, rbx
    mov rbx, rdx

    inc rcx

    push rcx
    push rbx
    push rax

    cmp rcx, 0xfffff
    jne loop

    nop
    hlt
"""

    code, _ = ks.asm(fib)
    assert isinstance(code, list)
    code = bytearray(code)
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    INSNS = [i for i in cs.disasm(code, 0)]
    emulate(code)
