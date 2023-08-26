import bochscpu


def dump_registers(state: bochscpu.State, include_kernel: bool = False):
    """
    Print registers for a given `State` in a WinDbg display type
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
dr6={state.dr6:016x}  dr7={state.dr7:016x}  efer={state.efer:016x}
"""
    )
    return
