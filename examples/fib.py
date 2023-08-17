import ctypes
import dataclasses
import platform
import struct
import time

import capstone
import keystone

import bochscpu

DEBUG = True
PAGE_SIZE = bochscpu.memory.PageSize()


@dataclasses.dataclass
class Stats:
    insn_nb: int = 0
    mem_access: list[int] = dataclasses.field(default_factory=lambda: [0, 0, 0])


stats = Stats()


def dbg(x: str):
    if DEBUG:
        print(f"[Py] {x}")


def mmap(sz: int = PAGE_SIZE, perm: str = "rw"):
    PROT_READ = 0x1
    PROT_WRITE = 0x2
    PROT_EXEC = 0x4
    MAP_PRIVATE = 0x2
    MAP_ANONYMOUS = 0x20
    libc = ctypes.CDLL("libc.so.6")
    mmap = libc.mmap
    mmap.restype = ctypes.c_void_p
    mmap.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_long]
    flags = 0
    match perm:
        case "ro":
            flags = PROT_READ
        case "rw":
            flags = PROT_READ | PROT_WRITE
        case "rwx":
            flags = PROT_READ | PROT_WRITE | PROT_EXECUTE
        case _:
            raise ValueError
    return mmap(-1, sz, flags, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0)


def VirtualAlloc(sz: int = PAGE_SIZE, perm: str = "rw"):
    if platform.system() == "Linux":
        return mmap(sz, perm)
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

    for i in range(0, PAGE_SIZE, 8):
        data = bytes(bochscpu.bochscpu_mem_phy_read(addr + i, 8))
        entry = struct.unpack("<Q", data[:8])[0]
        flags = entry & 0xFFF
        entry = entry & ~0xFFF
        if entry == 0:
            continue
        print(f"{' '*level} #{i//8} - {hex(entry)}|{flags=:#x}")
        dump_page_table(entry, level + 1)


def dump_registers(state: bochscpu.State, type: int = 0):
    # UM
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

    if type < 1:
        return

    # KM
    print(
        f"""
cr0={state.cr0:016x}  cr2={state.cr2:016x}  cr3={state.cr3:016x}  cr4={state.cr4:016x}
dr0={state.dr0:016x}  dr1={state.dr1:016x}  dr2={state.dr2:016x}  dr3={state.dr3:016x}
dr6={state.dr6:016x}  dr7={state.dr7:016x}  efer={state.efer:016x}
"""
    )


def missing_page_cb(gpa):
    raise Exception(f"missing_page_cb({gpa=:#x})")


def exception_cb(sess: bochscpu.session, cpu_id: int, vector: int, error_code: int):
    dbg(f"received exception({vector=:d}, {error_code=:d}) from cpu#{cpu_id}")
    sess.stop()


def lin_access_cb(
    sess: bochscpu.session,
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


def after_execution_cb(sess: bochscpu.session, cpu_id: int, insn: int):
    global stats
    stats.insn_nb += 1


def emulate(code: bytes):
    CODE = 0
    RW = 1

    #
    # Setup the PF handler very early to let Python handle it, rather than rust panicking
    #
    sess = bochscpu.session()
    dbg("registering our own missing page handler")
    sess.missing_page_handler = missing_page_cb

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

    cr4 = bochscpu.cpu.ControlRegister()
    cr4.PAE = True  # required for long mode

    #
    # Manually craft the guest virtual & physical memory layout into a pagetable
    # Once done bind the resulting GPAs it to bochs
    #
    shellcode_hva = VirtualAlloc()
    shellcode_gva = 0x0400_0000
    shellcode_gpa = 0x1400_0000
    dbg(f"inserting {shellcode_gva=:#x} -> {shellcode_gpa=:#x} ->  {shellcode_hva=:#x}")
    bochscpu.bochscpu_mem_page_insert(shellcode_gpa, shellcode_hva)

    stack_hva = VirtualAlloc()
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
    cpu = sess.cpu
    dbg(f"created cpu#{cpu.id}")

    state = bochscpu.State()
    state.rsp = stack_gva + PAGE_SIZE // 2
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
    sess.cpu.state = state
    dbg("loaded state for cpu#0")
    dbg("dumping start state")
    dump_registers(state)

    hooks = []
    hook = bochscpu.Hook()
    hook.exception = exception_cb
    hook.after_execution = after_execution_cb
    hook.lin_access = lin_access_cb
    hooks.append(hook)
    dbg("hooks ok")

    dbg("starting the vm...")
    t1 = time.time_ns()
    sess.run(hooks)
    t2 = time.time_ns()
    dbg(f"vm stopped, execution: {stats.insn_nb} insns in {t2-t1}ns")
    dbg(
        f"mem accesses: read={stats.mem_access[0]} write={stats.mem_access[1]} execute={stats.mem_access[2]}"
    )

    if stats.insn_nb < len(INSNS):
        dbg(f"last insn executed: {INSNS[stats.insn_nb]}")
    if stats.insn_nb - 1 < len(INSNS):
        dbg(f"next insn: {INSNS[stats.insn_nb+1]}")

    dbg("reading new state")
    new_state = sess.cpu.state
    dbg("dumping final state")
    dump_registers(new_state)
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

    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    code, _ = ks.asm(fib)
    assert isinstance(code, list)
    code = bytearray(code)
    INSNS = [i for i in cs.disasm(code, 0)]
    emulate(code)
