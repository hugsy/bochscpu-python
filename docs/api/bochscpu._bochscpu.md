<!-- markdownlint-disable -->

# <kbd>module</kbd> `bochscpu._bochscpu`
The native `bochscpu` module 

**Global Variables**
---------------
- **memory**
- **cpu**
- **BX_INSTR_IS_JMP**
- **BOCHSCPU_INSTR_IS_JMP_INDIRECT**
- **BOCHSCPU_INSTR_IS_CALL**
- **BOCHSCPU_INSTR_IS_CALL_INDIRECT**
- **BOCHSCPU_INSTR_IS_RET**
- **BOCHSCPU_INSTR_IS_IRET**
- **BOCHSCPU_INSTR_IS_INT**
- **BOCHSCPU_INSTR_IS_SYSCALL**
- **BOCHSCPU_INSTR_IS_SYSRET**
- **BOCHSCPU_INSTR_IS_SYSENTER**
- **BOCHSCPU_INSTR_IS_SYSEXIT**
- **BOCHSCPU_HOOK_MEM_READ**
- **BOCHSCPU_HOOK_MEM_WRITE**
- **BOCHSCPU_HOOK_MEM_EXECUTE**
- **BOCHSCPU_HOOK_MEM_RW**
- **BOCHSCPU_HOOK_TLB_CR0**
- **BOCHSCPU_HOOK_TLB_CR3**
- **BOCHSCPU_HOOK_TLB_CR4**
- **BOCHSCPU_HOOK_TLB_TASKSWITCH**
- **BOCHSCPU_HOOK_TLB_CONTEXTSWITCH**
- **BOCHSCPU_HOOK_TLB_INVLPG**
- **BOCHSCPU_HOOK_TLB_INVEPT**
- **BOCHSCPU_HOOK_TLB_INVVPID**
- **BOCHSCPU_HOOK_TLB_INVPCID**
- **BOCHSCPU_OPCODE_ERROR**
- **BOCHSCPU_OPCODE_INSERTED**


---

## <kbd>class</kbd> `GlobalSegment`
GlobalSegment class 


---

#### <kbd>property</kbd> GlobalSegment.base

Get/Set the GlobalSegment `base` attribute 

---

#### <kbd>property</kbd> GlobalSegment.limit

Get/Set the GlobalSegment `limit` attribute 




---

## <kbd>class</kbd> `Hook`
Class Hook 


---

#### <kbd>property</kbd> Hook.after_execution

Callback for Bochs `after_execution` callback 

---

#### <kbd>property</kbd> Hook.before_execution

Callback for Bochs `before_execution` callback 

---

#### <kbd>property</kbd> Hook.cache_cntrl

Callback for Bochs `cache_cntrl` callback 

---

#### <kbd>property</kbd> Hook.clflush

Callback for Bochs `clflush` callback 

---

#### <kbd>property</kbd> Hook.cnear_branch_not_taken

Callback for Bochs `cnear_branch_not_taken` callback 

---

#### <kbd>property</kbd> Hook.cnear_branch_taken

Callback for Bochs `cnear_branch_taken` callback 

---

#### <kbd>property</kbd> Hook.ctx

A raw pointer to the Session object 

---

#### <kbd>property</kbd> Hook.exception

Callback for Bochs `exception` callback 

---

#### <kbd>property</kbd> Hook.far_branch

Callback for Bochs `far_branch` callback 

---

#### <kbd>property</kbd> Hook.hlt

Callback for Bochs `hlt` callback 

---

#### <kbd>property</kbd> Hook.hw_interrupt

Callback for Bochs `hw_interrupt` callback 

---

#### <kbd>property</kbd> Hook.inp

Callback for Bochs `inp` callback 

---

#### <kbd>property</kbd> Hook.inp2

Callback for Bochs `inp2` callback 

---

#### <kbd>property</kbd> Hook.interrupt

Callback for Bochs `interrupt` callback 

---

#### <kbd>property</kbd> Hook.lin_access

Callback for Bochs `lin_access` callback 

---

#### <kbd>property</kbd> Hook.mwait

Callback for Bochs `mwait` callback 

---

#### <kbd>property</kbd> Hook.opcode

Callback for Bochs `opcode` callback 

---

#### <kbd>property</kbd> Hook.outp

Callback for Bochs `outp` callback 

---

#### <kbd>property</kbd> Hook.phy_access

Callback for Bochs `phy_access` callback 

---

#### <kbd>property</kbd> Hook.prefetch_hint

Callback for Bochs `prefetch_hint` callback 

---

#### <kbd>property</kbd> Hook.repeat_iteration

Callback for Bochs `repeat_iteration` callback 

---

#### <kbd>property</kbd> Hook.reset

Callback for Bochs `reset` callback 

---

#### <kbd>property</kbd> Hook.tlb_cntrl

Callback for Bochs `tlb_cntrl` callback 

---

#### <kbd>property</kbd> Hook.ucnear_branch

Callback for Bochs `ucnear_branch` callback 

---

#### <kbd>property</kbd> Hook.vmexit

Callback for Bochs `vmexit` callback 

---

#### <kbd>property</kbd> Hook.wrmsr

Callback for Bochs `wrmsr` callback 




---

## <kbd>class</kbd> `HookType`








---

## <kbd>class</kbd> `InstructionType`








---

## <kbd>class</kbd> `OpcodeOperationType`








---

## <kbd>class</kbd> `Segment`
Segment class 


---

#### <kbd>property</kbd> Segment.attr

Get/Set the Segment `attr` attribute 

---

#### <kbd>property</kbd> Segment.base

Get/Set the Segment `base` attribute 

---

#### <kbd>property</kbd> Segment.limit

Get/Set the Segment `limit` attribute 

---

#### <kbd>property</kbd> Segment.present

Get/Set the Segment `present` attribute 

---

#### <kbd>property</kbd> Segment.selector

Get/Set the Segment `selector` attribute 




---

## <kbd>class</kbd> `Session`
Class session 


---

#### <kbd>property</kbd> Session.cpu

Get the CPU associated to the session 

---

#### <kbd>property</kbd> Session.missing_page_handler

Set the missing page callback 


---

#### <kbd>handler</kbd> Session.run

---

#### <kbd>handler</kbd> Session.stop



---

## <kbd>class</kbd> `State`
Class State 


---

#### <kbd>property</kbd> State.apic_base

Get/Set the register `apic_base` in the current state 

---

#### <kbd>property</kbd> State.cr0

Get/Set the register `cr0` in the current state 

---

#### <kbd>property</kbd> State.cr2

Get/Set the register `cr2` in the current state 

---

#### <kbd>property</kbd> State.cr3

Get/Set the register `cr3` in the current state 

---

#### <kbd>property</kbd> State.cr4

Get/Set the register `cr4` in the current state 

---

#### <kbd>property</kbd> State.cr8

Get/Set the register `cr8` in the current state 

---

#### <kbd>property</kbd> State.cs

Get/Set the register `cs` in the current state 

---

#### <kbd>property</kbd> State.cstar

Get/Set the register `cstar` in the current state 

---

#### <kbd>property</kbd> State.dr0

Get/Set the register `dr0` in the current state 

---

#### <kbd>property</kbd> State.dr1

Get/Set the register `dr1` in the current state 

---

#### <kbd>property</kbd> State.dr2

Get/Set the register `dr2` in the current state 

---

#### <kbd>property</kbd> State.dr3

Get/Set the register `dr3` in the current state 

---

#### <kbd>property</kbd> State.dr6

Get/Set the register `dr6` in the current state 

---

#### <kbd>property</kbd> State.dr7

Get/Set the register `dr7` in the current state 

---

#### <kbd>property</kbd> State.ds

Get/Set the register `ds` in the current state 

---

#### <kbd>property</kbd> State.efer

Get/Set the register `efer` in the current state 

---

#### <kbd>property</kbd> State.es

Get/Set the register `es` in the current state 

---

#### <kbd>property</kbd> State.fpcw

Get/Set the register `fpcw` in the current state 

---

#### <kbd>property</kbd> State.fpop

Get/Set the register `fpop` in the current state 

---

#### <kbd>property</kbd> State.fpst

Get/Set the register `fpst` in the current state 

---

#### <kbd>property</kbd> State.fpsw

Get/Set the register `fpsw` in the current state 

---

#### <kbd>property</kbd> State.fptw

Get/Set the register `fptw` in the current state 

---

#### <kbd>property</kbd> State.fs

Get/Set the register `fs` in the current state 

---

#### <kbd>property</kbd> State.gdtr

Get/Set the register `gdtr` in the current state 

---

#### <kbd>property</kbd> State.gs

Get/Set the register `gs` in the current state 

---

#### <kbd>property</kbd> State.idtr

Get/Set the register `idtr` in the current state 

---

#### <kbd>property</kbd> State.kernel_gs_base

Get/Set the register `kernel_gs_base` in the current state 

---

#### <kbd>property</kbd> State.ldtr

Get/Set the register `ldtr` in the current state 

---

#### <kbd>property</kbd> State.lstar

Get/Set the register `lstar` in the current state 

---

#### <kbd>property</kbd> State.mxcsr

Get/Set the register `mxcsr` in the current state 

---

#### <kbd>property</kbd> State.mxcsr_mask

Get/Set the register `mxcsr_mask` in the current state 

---

#### <kbd>property</kbd> State.pat

Get/Set the register `pat` in the current state 

---

#### <kbd>property</kbd> State.r10

Get/Set the register `r10` in the current state 

---

#### <kbd>property</kbd> State.r11

Get/Set the register `r11` in the current state 

---

#### <kbd>property</kbd> State.r12

Get/Set the register `r12` in the current state 

---

#### <kbd>property</kbd> State.r13

Get/Set the register `r13` in the current state 

---

#### <kbd>property</kbd> State.r14

Get/Set the register `r14` in the current state 

---

#### <kbd>property</kbd> State.r15

Get/Set the register `r15` in the current state 

---

#### <kbd>property</kbd> State.r8

Get/Set the register `r8` in the current state 

---

#### <kbd>property</kbd> State.r9

Get/Set the register `r9` in the current state 

---

#### <kbd>property</kbd> State.rax

Get/Set the register `rax` in the current state 

---

#### <kbd>property</kbd> State.rbp

Get/Set the register `rbp` in the current state 

---

#### <kbd>property</kbd> State.rbx

Get/Set the register `rbx` in the current state 

---

#### <kbd>property</kbd> State.rcx

Get/Set the register `rcx` in the current state 

---

#### <kbd>property</kbd> State.rdi

Get/Set the register `rdi` in the current state 

---

#### <kbd>property</kbd> State.rdx

Get/Set the register `rdx` in the current state 

---

#### <kbd>property</kbd> State.rflags

Get/Set the register `rflags` in the current state 

---

#### <kbd>property</kbd> State.rip

Get/Set the register `rip` in the current state 

---

#### <kbd>property</kbd> State.rsi

Get/Set the register `rsi` in the current state 

---

#### <kbd>property</kbd> State.rsp

Get/Set the register `rsp` in the current state 

---

#### <kbd>property</kbd> State.seed

Get/Set the seed in the current state 

---

#### <kbd>property</kbd> State.sfmask

Get/Set the register `sfmask` in the current state 

---

#### <kbd>property</kbd> State.ss

Get/Set the register `ss` in the current state 

---

#### <kbd>property</kbd> State.star

Get/Set the register `star` in the current state 

---

#### <kbd>property</kbd> State.sysenter_cs

Get/Set the register `sysenter_cs` in the current state 

---

#### <kbd>property</kbd> State.sysenter_eip

Get/Set the register `sysenter_eip` in the current state 

---

#### <kbd>property</kbd> State.sysenter_esp

Get/Set the register `sysenter_esp` in the current state 

---

#### <kbd>property</kbd> State.tr

Get/Set the register `tr` in the current state 

---

#### <kbd>property</kbd> State.tsc

Get/Set the register `tsc` in the current state 

---

#### <kbd>property</kbd> State.tsc_aux

Get/Set the register `tsc_aux` in the current state 

---

#### <kbd>property</kbd> State.xcr0

Get/Set the register `xcr0` in the current state 

---

#### <kbd>property</kbd> State.zmm

Get/Set the register `zmm` in the current state 




---

## <kbd>class</kbd> `Zmm`





---

#### <kbd>property</kbd> Zmm.q

(self) -> list[int] 






---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
