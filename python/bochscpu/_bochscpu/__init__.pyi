from typing import Callable
from enum import Enum
import bochscpu._bochscpu.cpu

class GlobalSegment:
    """
    GlobalSegment class
    """

    def __init__(self) -> None: ...
    @property
    def base(self) -> int:
        """
        Get the GlobalSegment `base` attribute
        """
        ...
    @base.setter
    def base(self) -> int:
        """
        Set the GlobalSegment `base` attribute
        """
        ...
    @property
    def limit(self) -> int:
        """
        Get the GlobalSegment `limit` attribute
        """
        ...
    @limit.setter
    def limit(self) -> int:
        """
        Set the GlobalSegment `limit` attribute
        """
        ...

class HookType(Enum):
    """
    <attribute '__doc__' of 'HookType' objects>
    """

    MEM_EXECUTE: HookType
    MEM_READ: HookType
    MEM_RW: HookType
    MEM_WRITE: HookType
    TLB_CONTEXTSWITCH: HookType
    TLB_CR0: HookType
    TLB_CR3: HookType
    TLB_CR4: HookType
    TLB_INVEPT: HookType
    TLB_INVLPG: HookType
    TLB_INVPCID: HookType
    TLB_INVVPID: HookType
    TLB_TASKSWITCH: HookType

class InstructionType(Enum):
    IS_CALL: InstructionType
    IS_CALL_INDIRECT: InstructionType
    IS_INT: InstructionType
    IS_IRET: InstructionType
    IS_JMP: InstructionType
    IS_JMP_INDIRECT: InstructionType
    IS_RET: InstructionType
    IS_SYSCALL: InstructionType
    IS_SYSENTER: InstructionType
    IS_SYSEXIT: InstructionType
    IS_SYSRET: InstructionType

class OpcodeOperationType(Enum):
    OPERATION_ERROR: OpcodeOperationType
    OPERATION_INSERTED: OpcodeOperationType

class Segment:
    """
    Segment class
    """

    def __init__(self) -> None: ...
    @property
    def attr(self) -> int:
        """
        Get/Set the Segment `attr` attribute
        """
        ...
    @attr.setter
    def attr(self) -> int:
        """
        Get/Set the Segment `attr` attribute
        """
        ...
    @property
    def base(self) -> int:
        """
        Get/Set the Segment `base` attribute
        """
        ...
    @base.setter
    def base(self) -> int:
        """
        Get/Set the Segment `base` attribute
        """
        ...
    @property
    def limit(self) -> int:
        """
        Get/Set the Segment `limit` attribute
        """
        ...
    @limit.setter
    def limit(self) -> int:
        """
        Get/Set the Segment `limit` attribute
        """
        ...
    @property
    def present(self) -> bool:
        """
        Get/Set the Segment `present` attribute
        """
        ...
    @present.setter
    def present(self) -> bool:
        """
        Get/Set the Segment `present` attribute
        """
        ...
    @property
    def selector(self) -> int:
        """
        Get/Set the Segment `selector` attribute
        """
        ...
    @selector.setter
    def selector(self) -> int:
        """
        Get/Set the Segment `selector` attribute
        """
        ...
    def __int__(self) -> int:
        """Get the selector value as an integer"""
        ...

class State:
    """
    Class State
    """

    def __init__(self) -> None: ...
    @property
    def apic_base(self) -> int:
        """Get/Set the register `apic_base` in the current state"""
        ...
    @apic_base.setter
    def apic_base(self) -> int:
        """Get/Set the register `apic_base` in the current state"""
        ...
    @property
    def cr0(self) -> int:
        """Get/Set the register `cr0` in the current state"""
        ...
    @cr0.setter
    def cr0(self) -> int:
        """Get/Set the register `cr0` in the current state"""
        ...
    @property
    def cr2(self) -> int:
        """Get/Set the register `cr2` in the current state"""
        ...
    @cr2.setter
    def cr2(self) -> int:
        """Get/Set the register `cr2` in the current state"""
        ...
    @property
    def cr3(self) -> int:
        """Get/Set the register `cr3` in the current state"""
        ...
    @cr3.setter
    def cr3(self) -> int:
        """Get/Set the register `cr3` in the current state"""
        ...
    @property
    def cr4(self) -> int:
        """Get/Set the register `cr4` in the current state"""
        ...
    @cr4.setter
    def cr4(self) -> int:
        """Get/Set the register `cr4` in the current state"""
        ...
    @property
    def cr8(self) -> int:
        """Get/Set the register `cr8` in the current state"""
        ...
    @cr8.setter
    def cr8(self) -> int:
        """Get/Set the register `cr8` in the current state"""
        ...
    @property
    def cs(self) -> bochscpu._bochscpu.Segment:
        """Get/Set the register `cs` in the current state"""
        ...
    @cs.setter
    def cs(self) -> bochscpu._bochscpu.Segment:
        """Get/Set the register `cs` in the current state"""
        ...
    @property
    def cstar(self) -> int:
        """Get/Set the register `cstar` in the current state"""
        ...
    @cstar.setter
    def cstar(self) -> int:
        """Get/Set the register `cstar` in the current state"""
        ...
    @property
    def dr0(self) -> int:
        """Get/Set the register `dr0` in the current state"""
        ...
    @dr0.setter
    def dr0(self) -> int:
        """
        Get/Set the register `dr0` in the current state
        """
        ...
    @property
    def dr1(self) -> int:
        """
        Get/Set the register `dr1` in the current state
        """
        ...
    @dr1.setter
    def dr1(self) -> int:
        """
        Get/Set the register `dr1` in the current state
        """
        ...
    @property
    def dr2(self) -> int:
        """
        Get/Set the register `dr2` in the current state
        """
        ...
    @dr2.setter
    def dr2(self) -> int:
        """
        Get/Set the register `dr2` in the current state
        """
        ...
    @property
    def dr3(self) -> int:
        """
        Get/Set the register `dr3` in the current state
        """
        ...
    @dr3.setter
    def dr3(self) -> int:
        """
        Get/Set the register `dr3` in the current state
        """
        ...
    @property
    def dr6(self) -> int:
        """
        Get/Set the register `dr6` in the current state
        """
        ...
    @dr6.setter
    def dr6(self) -> int:
        """
        Get/Set the register `dr6` in the current state
        """
        ...
    @property
    def dr7(self) -> int:
        """
        Get/Set the register `dr7` in the current state
        """
        ...
    @dr7.setter
    def dr7(self) -> int:
        """
        Get/Set the register `dr7` in the current state
        """
        ...
    @property
    def ds(self) -> bochscpu._bochscpu.Segment:
        """
        Get/Set the register `ds` in the current state
        """
        ...
    @ds.setter
    def ds(self) -> bochscpu._bochscpu.Segment:
        """
        Get/Set the register `ds` in the current state
        """
        ...
    @property
    def efer(self) -> int:
        """
        Get/Set the register `efer` in the current state
        """
        ...
    @efer.setter
    def efer(self) -> int:
        """
        Get/Set the register `efer` in the current state
        """
        ...
    @property
    def es(self) -> bochscpu._bochscpu.Segment:
        """
        Get/Set the register `es` in the current state
        """
        ...
    @es.setter
    def es(self) -> bochscpu._bochscpu.Segment:
        """
        Get/Set the register `es` in the current state
        """
        ...
    @property
    def fpcw(self) -> int:
        """
        Get/Set the register `fpcw` in the current state
        """
        ...
    @fpcw.setter
    def fpcw(self) -> int:
        """
        Get/Set the register `fpcw` in the current state
        """
        ...
    @property
    def fpop(self) -> int:
        """
        Get/Set the register `fpop` in the current state
        """
        ...
    @fpop.setter
    def fpop(self) -> int:
        """
        Get/Set the register `fpop` in the current state
        """
        ...
    @property
    def fpst(self) -> list[int]:
        """
        Get/Set the register `fpst` in the current state
        """
        ...
    @fpst.setter
    def fpst(self) -> list[int]:
        """
        Get/Set the register `fpst` in the current state
        """
        ...
    @property
    def fpsw(self) -> int:
        """
        Get/Set the register `fpsw` in the current state
        """
        ...
    @fpsw.setter
    def fpsw(self) -> int:
        """
        Get/Set the register `fpsw` in the current state
        """
        ...
    @property
    def fptw(self) -> int:
        """
        Get/Set the register `fptw` in the current state
        """
        ...
    @fptw.setter
    def fptw(self) -> int:
        """
        Get/Set the register `fptw` in the current state
        """
        ...
    @property
    def fs(self) -> bochscpu._bochscpu.Segment:
        """
        Get/Set the register `fs` in the current state
        """
        ...
    @fs.setter
    def fs(self) -> bochscpu._bochscpu.Segment:
        """
        Get/Set the register `fs` in the current state
        """
        ...
    @property
    def gdtr(self) -> bochscpu._bochscpu.GlobalSegment:
        """
        Get/Set the register `gdtr` in the current state
        """
        ...
    @gdtr.setter
    def gdtr(self) -> bochscpu._bochscpu.GlobalSegment:
        """
        Get/Set the register `gdtr` in the current state
        """
        ...
    @property
    def gs(self) -> bochscpu._bochscpu.Segment:
        """
        Get/Set the register `gs` in the current state
        """
        ...
    @gs.setter
    def gs(self) -> bochscpu._bochscpu.Segment:
        """
        Get/Set the register `gs` in the current state
        """
        ...
    @property
    def idtr(self) -> bochscpu._bochscpu.GlobalSegment:
        """
        Get/Set the register `idtr` in the current state
        """
        ...
    @idtr.setter
    def idtr(self) -> bochscpu._bochscpu.GlobalSegment:
        """
        Get/Set the register `idtr` in the current state
        """
        ...
    @property
    def kernel_gs_base(self) -> int:
        """
        Get/Set the register `kernel_gs_base` in the current state
        """
        ...
    @kernel_gs_base.setter
    def kernel_gs_base(self) -> int:
        """
        Get/Set the register `kernel_gs_base` in the current state
        """
        ...
    @property
    def ldtr(self) -> bochscpu._bochscpu.Segment:
        """
        Get/Set the register `ldtr` in the current state
        """
        ...
    @ldtr.setter
    def ldtr(self) -> bochscpu._bochscpu.Segment:
        """
        Get/Set the register `ldtr` in the current state
        """
        ...
    @property
    def lstar(self) -> int:
        """
        Get/Set the register `lstar` in the current state
        """
        ...
    @lstar.setter
    def lstar(self) -> int:
        """
        Get/Set the register `lstar` in the current state
        """
        ...
    @property
    def mxcsr(self) -> int:
        """
        Get/Set the register `mxcsr` in the current state
        """
        ...
    @mxcsr.setter
    def mxcsr(self) -> int:
        """
        Get/Set the register `mxcsr` in the current state
        """
        ...
    @property
    def mxcsr_mask(self) -> int:
        """
        Get/Set the register `mxcsr_mask` in the current state
        """
        ...
    @mxcsr_mask.setter
    def mxcsr_mask(self) -> int:
        """
        Get/Set the register `mxcsr_mask` in the current state
        """
        ...
    @property
    def pat(self) -> int:
        """
        Get/Set the register `pat` in the current state
        """
        ...
    @pat.setter
    def pat(self) -> int:
        """
        Get/Set the register `pat` in the current state
        """
        ...
    @property
    def r10(self) -> int:
        """
        Get/Set the register `r10` in the current state
        """
        ...
    @r10.setter
    def r10(self) -> int:
        """
        Get/Set the register `r10` in the current state
        """
        ...
    @property
    def r11(self) -> int:
        """
        Get/Set the register `r11` in the current state
        """
        ...
    @r11.setter
    def r11(self) -> int:
        """
        Get/Set the register `r11` in the current state
        """
        ...
    @property
    def r12(self) -> int:
        """
        Get/Set the register `r12` in the current state
        """
        ...
    @r12.setter
    def r12(self) -> int:
        """
        Get/Set the register `r12` in the current state
        """
        ...
    @property
    def r13(self) -> int:
        """
        Get/Set the register `r13` in the current state
        """
        ...
    @r13.setter
    def r13(self) -> int:
        """
        Get/Set the register `r13` in the current state
        """
        ...
    @property
    def r14(self) -> int:
        """
        Get/Set the register `r14` in the current state
        """
        ...
    @r14.setter
    def r14(self) -> int:
        """
        Get/Set the register `r14` in the current state
        """
        ...
    @property
    def r15(self) -> int:
        """
        Get/Set the register `r15` in the current state
        """
        ...
    @r15.setter
    def r15(self) -> int:
        """
        Get/Set the register `r15` in the current state
        """
        ...
    @property
    def r8(self) -> int:
        """
        Get/Set the register `r8` in the current state
        """
        ...
    @r8.setter
    def r8(self) -> int:
        """
        Get/Set the register `r8` in the current state
        """
        ...
    @property
    def r9(self) -> int:
        """
        Get/Set the register `r9` in the current state
        """
        ...
    @r9.setter
    def r9(self) -> int:
        """
        Get/Set the register `r9` in the current state
        """
        ...
    @property
    def rax(self) -> int:
        """
        Get/Set the register `rax` in the current state
        """
        ...
    @rax.setter
    def rax(self) -> int:
        """
        Get/Set the register `rax` in the current state
        """
        ...
    @property
    def rbp(self) -> int:
        """
        Get/Set the register `rbp` in the current state
        """
        ...
    @rbp.setter
    def rbp(self) -> int:
        """
        Get/Set the register `rbp` in the current state
        """
        ...
    @property
    def rbx(self) -> int:
        """
        Get/Set the register `rbx` in the current state
        """
        ...
    @rbx.setter
    def rbx(self) -> int:
        """
        Get/Set the register `rbx` in the current state
        """
        ...
    @property
    def rcx(self) -> int:
        """
        Get/Set the register `rcx` in the current state
        """
        ...
    @rcx.setter
    def rcx(self) -> int:
        """
        Get/Set the register `rcx` in the current state
        """
        ...
    @property
    def rdi(self) -> int:
        """
        Get/Set the register `rdi` in the current state
        """
        ...
    @rdi.setter
    def rdi(self) -> int:
        """
        Get/Set the register `rdi` in the current state
        """
        ...
    @property
    def rdx(self) -> int:
        """
        Get/Set the register `rdx` in the current state
        """
        ...
    @rdx.setter
    def rdx(self) -> int:
        """
        Get/Set the register `rdx` in the current state
        """
        ...
    @property
    def rflags(self) -> int:
        """
        Get/Set the register `rflags` in the current state
        """
        ...
    @rflags.setter
    def rflags(self) -> int:
        """
        Get/Set the register `rflags` in the current state
        """
        ...
    @property
    def rip(self) -> int:
        """
        Get/Set the register `rip` in the current state
        """
        ...
    @rip.setter
    def rip(self) -> int:
        """
        Get/Set the register `rip` in the current state
        """
        ...
    @property
    def rsi(self) -> int:
        """
        Get/Set the register `rsi` in the current state
        """
        ...
    @rsi.setter
    def rsi(self) -> int:
        """
        Get/Set the register `rsi` in the current state
        """
        ...
    @property
    def rsp(self) -> int:
        """
        Get/Set the register `rsp` in the current state
        """
        ...
    @rsp.setter
    def rsp(self) -> int:
        """
        Get/Set the register `rsp` in the current state
        """
        ...
    @property
    def seed(self) -> int:
        """
        Get/Set the seed in the current state
        """
        ...
    @seed.setter
    def seed(self) -> int:
        """
        Get/Set the seed in the current state
        """
        ...
    @property
    def sfmask(self) -> int:
        """
        Get/Set the register `sfmask` in the current state
        """
        ...
    @sfmask.setter
    def sfmask(self) -> int:
        """
        Get/Set the register `sfmask` in the current state
        """
        ...
    @property
    def ss(self) -> bochscpu._bochscpu.Segment:
        """
        Get/Set the register `ss` in the current state
        """
        ...
    @ss.setter
    def ss(self) -> bochscpu._bochscpu.Segment:
        """
        Get/Set the register `ss` in the current state
        """
        ...
    @property
    def star(self) -> int:
        """
        Get/Set the register `star` in the current state
        """
        ...
    @star.setter
    def star(self) -> int:
        """
        Get/Set the register `star` in the current state
        """
        ...
    @property
    def sysenter_cs(self) -> int:
        """
        Get/Set the register `sysenter_cs` in the current state
        """
        ...
    @sysenter_cs.setter
    def sysenter_cs(self) -> int:
        """
        Get/Set the register `sysenter_cs` in the current state
        """
        ...
    @property
    def sysenter_eip(self) -> int:
        """
        Get/Set the register `sysenter_eip` in the current state
        """
        ...
    @sysenter_eip.setter
    def sysenter_eip(self) -> int:
        """
        Get/Set the register `sysenter_eip` in the current state
        """
        ...
    @property
    def sysenter_esp(self) -> int:
        """
        Get/Set the register `sysenter_esp` in the current state
        """
        ...
    @sysenter_esp.setter
    def sysenter_esp(self) -> int:
        """
        Get/Set the register `sysenter_esp` in the current state
        """
        ...
    @property
    def tr(self) -> bochscpu._bochscpu.Segment:
        """
        Get/Set the register `tr` in the current state
        """
        ...
    @tr.setter
    def tr(self) -> bochscpu._bochscpu.Segment:
        """
        Get/Set the register `tr` in the current state
        """
        ...
    @property
    def tsc(self) -> int:
        """
        Get/Set the register `tsc` in the current state
        """
        ...
    @tsc.setter
    def tsc(self) -> int:
        """
        Get/Set the register `tsc` in the current state
        """
        ...
    @property
    def tsc_aux(self) -> int:
        """
        Get/Set the register `tsc_aux` in the current state
        """
        ...
    @tsc_aux.setter
    def tsc_aux(self) -> int:
        """
        Get/Set the register `tsc_aux` in the current state
        """
        ...
    @property
    def xcr0(self) -> int:
        """
        Get/Set the register `xcr0` in the current state
        """
        ...
    @xcr0.setter
    def xcr0(self) -> int:
        """
        Get/Set the register `xcr0` in the current state
        """
        ...
    @property
    def zmm(self) -> list[bochscpu._bochscpu.Zmm]:
        """
        Get/Set the register `zmm` in the current state
        """
        ...
    @zmm.setter
    def zmm(self) -> list[bochscpu._bochscpu.Zmm]:
        """
        Get/Set the register `zmm` in the current state
        """
        ...

TLB_CONTEXTSWITCH: HookType
TLB_CR0: HookType
TLB_CR3: HookType
TLB_CR4: HookType
TLB_INVEPT: HookType
TLB_INVLPG: HookType
TLB_INVPCID: HookType
TLB_INVVPID: HookType
TLB_TASKSWITCH: HookType

class Zmm:
    def __init__(self) -> None: ...
    @property
    def q(self) -> list[int]: ...
    @q.setter
    def q(self) -> list[int]: ...

def bochscpu_log_set_level(level: int) -> None:
    """
    Set verbosity level
    """
    ...

def instr_bx_opcode(p: int) -> int: ...
def instr_imm16(p: int) -> int: ...
def instr_imm32(p: int) -> int: ...
def instr_imm64(p: int) -> int: ...

class Session:
    """
    Class session
    """

    def __init__(self) -> None: ...
    @property
    def cpu(self) -> bochscpu._bochscpu.cpu.Cpu:
        """
        Get the CPU associated to the session
        """
        ...
    @property
    def missing_page_handler(self) -> Callable[[int, None], None]:
        """
        Set the missing page callback
        """
        ...
    @missing_page_handler.setter
    def missing_page_handler(self) -> Callable[[int, None], None]:
        """
        Get the missing page callback
        """
        ...
    def run(self, arg: list[bochscpu._bochscpu.Hook], /) -> None:
        """
        Start the execution with a set of hooks
        """
        ...
    def stop(self) -> None:
        """
        Stop the execution
        """
        ...

class Hook:
    """
    Class Hook
    """

    def __init__(self) -> None: ...
    @property
    def after_execution(self) -> Callable[[bochscpu._bochscpu.Session, int, int], None]:
        """
        Callback for Bochs `after_execution` callback
        """
        ...
    @after_execution.setter
    def after_execution(self) -> Callable[[bochscpu._bochscpu.Session, int, int], None]:
        """
        Callback for Bochs `after_execution` callback
        """
        ...
    @property
    def before_execution(
        self,
    ) -> Callable[[bochscpu._bochscpu.Session, int, int], None]:
        """
        Callback for Bochs `before_execution` callback
        """
        ...
    @before_execution.setter
    def before_execution(
        self,
    ) -> Callable[[bochscpu._bochscpu.Session, int, int], None]:
        """
        Callback for Bochs `before_execution` callback
        """
        ...
    @property
    def cache_cntrl(self) -> Callable[[bochscpu._bochscpu.Session, int, int], None]:
        """
        Callback for Bochs `cache_cntrl` callback
        """
        ...
    @cache_cntrl.setter
    def cache_cntrl(self) -> Callable[[bochscpu._bochscpu.Session, int, int], None]:
        """
        Callback for Bochs `cache_cntrl` callback
        """
        ...
    @property
    def clflush(self) -> Callable[[bochscpu._bochscpu.Session, int, int, int], None]:
        """
        Callback for Bochs `clflush` callback
        """
        ...
    @clflush.setter
    def clflush(self) -> Callable[[bochscpu._bochscpu.Session, int, int, int], None]:
        """
        Callback for Bochs `clflush` callback
        """
        ...
    @property
    def cnear_branch_not_taken(
        self,
    ) -> Callable[[bochscpu._bochscpu.Session, int, int, int], None]:
        """
        Callback for Bochs `cnear_branch_not_taken` callback
        """
        ...
    @cnear_branch_not_taken.setter
    def cnear_branch_not_taken(
        self,
    ) -> Callable[[bochscpu._bochscpu.Session, int, int, int], None]:
        """
        Callback for Bochs `cnear_branch_not_taken` callback
        """
        ...
    @property
    def cnear_branch_taken(
        self,
    ) -> Callable[[bochscpu._bochscpu.Session, int, int, int], None]:
        """
        Callback for Bochs `cnear_branch_taken` callback
        """
        ...
    @cnear_branch_taken.setter
    def cnear_branch_taken(
        self,
    ) -> Callable[[bochscpu._bochscpu.Session, int, int, int], None]:
        """
        Callback for Bochs `cnear_branch_taken` callback
        """
        ...
    @property
    def ctx(self) -> int:
        """
        A raw pointer to the Session object
        """
        ...
    @ctx.setter
    def ctx(self) -> int:
        """
        A raw pointer to the Session object
        """
        ...
    @property
    def exception(self) -> Callable[[bochscpu._bochscpu.Session, int, int, int], None]:
        """
        Callback for Bochs `exception` callback
        """
        ...
    @exception.setter
    def exception(self) -> Callable[[bochscpu._bochscpu.Session, int, int, int], None]:
        """
        Callback for Bochs `exception` callback
        """
        ...
    @property
    def far_branch(
        self,
    ) -> Callable[[bochscpu._bochscpu.Session, int, int, int, int, int, int], None]:
        """
        Callback for Bochs `far_branch` callback
        """
        ...
    @far_branch.setter
    def far_branch(
        self,
    ) -> Callable[[bochscpu._bochscpu.Session, int, int, int, int, int, int], None]:
        """
        Callback for Bochs `far_branch` callback
        """
        ...
    @property
    def hlt(self) -> Callable[[bochscpu._bochscpu.Session, int], None]:
        """
        Callback for Bochs `hlt` callback
        """
        ...
    @hlt.setter
    def hlt(self) -> Callable[[bochscpu._bochscpu.Session, int], None]:
        """
        Callback for Bochs `hlt` callback
        """
        ...
    @property
    def hw_interrupt(
        self,
    ) -> Callable[[bochscpu._bochscpu.Session, int, int, int, int], None]:
        """
        Callback for Bochs `hw_interrupt` callback
        """
        ...
    @hw_interrupt.setter
    def hw_interrupt(
        self,
    ) -> Callable[[bochscpu._bochscpu.Session, int, int, int, int], None]:
        """
        Callback for Bochs `hw_interrupt` callback
        """
        ...
    @property
    def inp(self) -> Callable[[bochscpu._bochscpu.Session, int, int], None]:
        """
        Callback for Bochs `inp` callback
        """
        ...
    @inp.setter
    def inp(self) -> Callable[[bochscpu._bochscpu.Session, int, int], None]:
        """
        Callback for Bochs `inp` callback
        """
        ...
    @property
    def inp2(self) -> Callable[[bochscpu._bochscpu.Session, int, int, int], None]:
        """
        Callback for Bochs `inp2` callback
        """
        ...
    @inp2.setter
    def inp2(self) -> Callable[[bochscpu._bochscpu.Session, int, int, int], None]:
        """
        Callback for Bochs `inp2` callback
        """
        ...
    @property
    def interrupt(self) -> Callable[[bochscpu._bochscpu.Session, int, int], None]:
        """
        Callback for Bochs `interrupt` callback
        """
        ...
    @interrupt.setter
    def interrupt(self) -> Callable[[bochscpu._bochscpu.Session, int, int], None]:
        """
        Callback for Bochs `interrupt` callback
        """
        ...
    @property
    def lin_access(
        self,
    ) -> Callable[[bochscpu._bochscpu.Session, int, int, int, int, int, int], None]:
        """
        Callback for Bochs `lin_access` callback
        """
        ...
    @lin_access.setter
    def lin_access(
        self,
    ) -> Callable[[bochscpu._bochscpu.Session, int, int, int, int, int, int], None]:
        """
        Callback for Bochs `lin_access` callback
        """
        ...
    @property
    def mwait(self) -> Callable[[bochscpu._bochscpu.Session, int, int, int, int], None]:
        """
        Callback for Bochs `mwait` callback
        """
        ...
    @mwait.setter
    def mwait(self) -> Callable[[bochscpu._bochscpu.Session, int, int, int, int], None]:
        """
        Callback for Bochs `mwait` callback
        """
        ...
    @property
    def opcode(
        self,
    ) -> Callable[[bochscpu._bochscpu.Session, int, int, int, int, bool, bool], None]:
        """
        Callback for Bochs `opcode` callback
        """
        ...
    @opcode.setter
    def opcode(
        self,
    ) -> Callable[[bochscpu._bochscpu.Session, int, int, int, int, bool, bool], None]:
        """
        Callback for Bochs `opcode` callback
        """
        ...
    @property
    def outp(self) -> Callable[[bochscpu._bochscpu.Session, int, int, int], None]:
        """
        Callback for Bochs `outp` callback
        """
        ...
    @outp.setter
    def outp(self) -> Callable[[bochscpu._bochscpu.Session, int, int, int], None]:
        """
        Callback for Bochs `outp` callback
        """
        ...
    @property
    def phy_access(
        self,
    ) -> Callable[[bochscpu._bochscpu.Session, int, int, int, int, int], None]:
        """
        Callback for Bochs `phy_access` callback
        """
        ...
    @phy_access.setter
    def phy_access(
        self,
    ) -> Callable[[bochscpu._bochscpu.Session, int, int, int, int, int], None]:
        """
        Callback for Bochs `phy_access` callback
        """
        ...
    @property
    def prefetch_hint(
        self,
    ) -> Callable[[bochscpu._bochscpu.Session, int, int, int, int], None]:
        """
        Callback for Bochs `prefetch_hint` callback
        """
        ...
    @prefetch_hint.setter
    def prefetch_hint(
        self,
    ) -> Callable[[bochscpu._bochscpu.Session, int, int, int, int], None]:
        """
        Callback for Bochs `prefetch_hint` callback
        """
        ...
    @property
    def repeat_iteration(
        self,
    ) -> Callable[[bochscpu._bochscpu.Session, int, int], None]:
        """
        Callback for Bochs `repeat_iteration` callback
        """
        ...
    @repeat_iteration.setter
    def repeat_iteration(
        self,
    ) -> Callable[[bochscpu._bochscpu.Session, int, int], None]:
        """
        Callback for Bochs `repeat_iteration` callback
        """
        ...
    @property
    def reset(self) -> Callable[[bochscpu._bochscpu.Session, int, int], None]:
        """
        Callback for Bochs `reset` callback
        """
        ...
    @reset.setter
    def reset(self) -> Callable[[bochscpu._bochscpu.Session, int, int], None]:
        """
        Callback for Bochs `reset` callback
        """
        ...
    @property
    def tlb_cntrl(self) -> Callable[[bochscpu._bochscpu.Session, int, int, int], None]:
        """
        Callback for Bochs `tlb_cntrl` callback
        """
        ...
    @tlb_cntrl.setter
    def tlb_cntrl(self) -> Callable[[bochscpu._bochscpu.Session, int, int, int], None]:
        """
        Callback for Bochs `tlb_cntrl` callback
        """
        ...
    @property
    def ucnear_branch(
        self,
    ) -> Callable[[bochscpu._bochscpu.Session, int, int, int, int], None]:
        """
        Callback for Bochs `ucnear_branch` callback
        """
        ...
    @ucnear_branch.setter
    def ucnear_branch(
        self,
    ) -> Callable[[bochscpu._bochscpu.Session, int, int, int, int], None]:
        """
        Callback for Bochs `ucnear_branch` callback
        """
        ...
    @property
    def vmexit(self) -> Callable[[bochscpu._bochscpu.Session, int, int, int], None]:
        """
        Callback for Bochs `vmexit` callback
        """
        ...
    @vmexit.setter
    def vmexit(self) -> Callable[[bochscpu._bochscpu.Session, int, int, int], None]:
        """
        Callback for Bochs `vmexit` callback
        """
        ...
    @property
    def wrmsr(self) -> Callable[[bochscpu._bochscpu.Session, int, int, int], None]:
        """
        Callback for Bochs `wrmsr` callback
        """
        ...
    @wrmsr.setter
    def wrmsr(self) -> Callable[[bochscpu._bochscpu.Session, int, int, int], None]:
        """
        Callback for Bochs `wrmsr` callback
        """
        ...
