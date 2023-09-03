from enum import Flag, Enum
import bochscpu._bochscpu

class ControlRegister:
    """
    ControlRegister class
    @ref AMD Manual Vol 2 - 3-1 (CR0)
    @ref AMD Manual Vol 2 - 3-7 (CR4)
    @ref AMD Manual Vol 2 - 3-8 (RFLAGS)
    @ref AMD Manual Vol 2 - 3-9 (EFER)
    """

    @property
    def AM(self) -> bool:
        """
        Get/Set AM control register flag: CR0 Alignment Mask R/W
        """
        ...
    @AM.setter
    def AM(self) -> bool:
        """
        Get/Set AM control register flag: CR0 Alignment Mask R/W
        """
        ...
    @property
    def CD(self) -> bool:
        """
        Get/Set CD control register flag: CR0 Cache Disable R/W
        """
        ...
    @CD.setter
    def CD(self) -> bool:
        """
        Get/Set CD control register flag: CR0 Cache Disable R/W
        """
        ...
    @property
    def DE(self) -> bool:
        """
        Get/Set DE control register flag: CR4 Debugging Extensions R/W
        """
        ...
    @DE.setter
    def DE(self) -> bool:
        """
        Get/Set DE control register flag: CR4 Debugging Extensions R/W
        """
        ...
    @property
    def EM(self) -> bool:
        """
        Get/Set EM control register flag: CR0 Emulation R/W
        """
        ...
    @EM.setter
    def EM(self) -> bool:
        """
        Get/Set EM control register flag: CR0 Emulation R/W
        """
        ...
    @property
    def ET(self) -> bool:
        """
        Get/Set ET control register flag: CR0 Extension Type R
        """
        ...
    @ET.setter
    def ET(self) -> bool:
        """
        Get/Set ET control register flag: CR0 Extension Type R
        """
        ...
    @property
    def FSGSBASE(self) -> bool:
        """
        Get/Set FSGSBASE control register flag: CR4 Enable RDFSBASE, RDGSBASE, WRFSBASE, and WRGSBASE instructions R/W
        """
        ...
    @FSGSBASE.setter
    def FSGSBASE(self) -> bool:
        """
        Get/Set FSGSBASE control register flag: CR4 Enable RDFSBASE, RDGSBASE, WRFSBASE, and WRGSBASE instructions R/W
        """
        ...
    @property
    def MCE(self) -> bool:
        """
        Get/Set MCE control register flag: CR4 Machine Check Enable R/W
        """
        ...
    @MCE.setter
    def MCE(self) -> bool:
        """
        Get/Set MCE control register flag: CR4 Machine Check Enable R/W
        """
        ...
    @property
    def MP(self) -> bool:
        """
        Get/Set MP control register flag: CR0 Monitor Coprocessor R/W
        """
        ...
    @MP.setter
    def MP(self) -> bool:
        """
        Get/Set MP control register flag: CR0 Monitor Coprocessor R/W
        """
        ...
    @property
    def NE(self) -> bool:
        """
        Get/Set NE control register flag: CR0 Numeric Error R/W
        """
        ...
    @NE.setter
    def NE(self) -> bool:
        """
        Get/Set NE control register flag: CR0 Numeric Error R/W
        """
        ...
    @property
    def NW(self) -> bool:
        """
        Get/Set NW control register flag: CR0 Not Writethrough R/W
        """
        ...
    @NW.setter
    def NW(self) -> bool:
        """
        Get/Set NW control register flag: CR0 Not Writethrough R/W
        """
        ...
    @property
    def OSFXSR(self) -> bool:
        """
        Get/Set OSFXSR control register flag: CR4 Operating System FXSAVE/FXRSTOR Support R/W
        """
        ...
    @OSFXSR.setter
    def OSFXSR(self) -> bool:
        """
        Get/Set OSFXSR control register flag: CR4 Operating System FXSAVE/FXRSTOR Support R/W
        """
        ...
    @property
    def OSXMMEXCPT(self) -> bool:
        """
        Get/Set OSXMMEXCPT control register flag: CR4 Operating System Unmasked Exception Support R/W
        """
        ...
    @OSXMMEXCPT.setter
    def OSXMMEXCPT(self) -> bool:
        """
        Get/Set OSXMMEXCPT control register flag: CR4 Operating System Unmasked Exception Support R/W
        """
        ...
    @property
    def OSXSAVE(self) -> bool:
        """
        Get/Set OSXSAVE control register flag: CR4 XSAVE and Processor Extended States Enable Bit R/W
        """
        ...
    @OSXSAVE.setter
    def OSXSAVE(self) -> bool:
        """
        Get/Set OSXSAVE control register flag: CR4 XSAVE and Processor Extended States Enable Bit R/W
        """
        ...
    @property
    def PAE(self) -> bool:
        """
        Get/Set PAE control register flag: CR4 Physical-Address Extension R/W
        """
        ...
    @PAE.setter
    def PAE(self) -> bool:
        """
        Get/Set PAE control register flag: CR4 Physical-Address Extension R/W
        """
        ...
    @property
    def PCE(self) -> bool:
        """
        Get/Set PCE control register flag: CR4 Performance-Monitoring Counter Enable R/W
        """
        ...
    @PCE.setter
    def PCE(self) -> bool:
        """
        Get/Set PCE control register flag: CR4 Performance-Monitoring Counter Enable R/W
        """
        ...
    @property
    def PE(self) -> bool:
        """
        Get/Set PE control register flag: CR0 Protection Enabled R/W
        """
        ...
    @PE.setter
    def PE(self) -> bool:
        """
        Get/Set PE control register flag: CR0 Protection Enabled R/W
        """
        ...
    @property
    def PG(self) -> bool:
        """
        Get/Set PG control register flag: CR0 Paging R/W
        """
        ...
    @PG.setter
    def PG(self) -> bool:
        """
        Get/Set PG control register flag: CR0 Paging R/W
        """
        ...
    @property
    def PGE(self) -> bool:
        """
        Get/Set PGE control register flag: CR4 Page-Global Enable R/W
        """
        ...
    @PGE.setter
    def PGE(self) -> bool:
        """
        Get/Set PGE control register flag: CR4 Page-Global Enable R/W
        """
        ...
    @property
    def PSE(self) -> bool:
        """
        Get/Set PSE control register flag: CR4 Page Size Extensions R/W
        """
        ...
    @PSE.setter
    def PSE(self) -> bool:
        """
        Get/Set PSE control register flag: CR4 Page Size Extensions R/W
        """
        ...
    @property
    def PVI(self) -> bool:
        """
        Get/Set PVI control register flag: CR4 Protected-Mode Virtual Interrupts R/W
        """
        ...
    @PVI.setter
    def PVI(self) -> bool:
        """
        Get/Set PVI control register flag: CR4 Protected-Mode Virtual Interrupts R/W
        """
        ...
    @property
    def TS(self) -> bool:
        """
        Get/Set TS control register flag: CR0 Task Switched R/W
        """
        ...
    @TS.setter
    def TS(self) -> bool:
        """
        Get/Set TS control register flag: CR0 Task Switched R/W
        """
        ...
    @property
    def TSD(self) -> bool:
        """
        Get/Set TSD control register flag: CR4 Time Stamp Disable R/W
        """
        ...
    @TSD.setter
    def TSD(self) -> bool:
        """
        Get/Set TSD control register flag: CR4 Time Stamp Disable R/W
        """
        ...
    @property
    def VME(self) -> bool:
        """
        Get/Set VME control register flag: CR4 Virtual-8086 Mode Extensions R/W
        """
        ...
    @VME.setter
    def VME(self) -> bool:
        """
        Get/Set VME control register flag: CR4 Virtual-8086 Mode Extensions R/W
        """
        ...
    @property
    def WP(self) -> bool:
        """
        Get/Set WP control register flag: CR0 Write Protect R/W
        """
        ...
    @WP.setter
    def WP(self) -> bool:
        """
        Get/Set WP control register flag: CR0 Write Protect R/W
        """
        ...
    @X.setter
    def X(self) -> bool:
        """Set the CR4 flag X"""
        ...
    @property
    def X(self) -> bool:
        """Get X CR4 Flag"""
        ...
    @LWP.setter
    def LWP(self) -> bool:
        """Set the CR4 flag LWP"""
        ...
    @property
    def LWP(self) -> bool:
        """Get LWP CR4 Flag"""
        ...
    @YMM.setter
    def YMM(self) -> bool:
        """Set the CR4 flag YMM"""
        ...
    @property
    def YMM(self) -> bool:
        """Get YMM CR4 Flag"""
        ...
    @SSE.setter
    def SSE(self) -> bool:
        """Set the CR4 flag SSE"""
        ...
    @property
    def SSE(self) -> bool:
        """Get SSE CR4 Flag"""
        ...
    @x87.setter
    def x87(self) -> bool:
        """Set the CR4 flag x87"""
        ...
    @property
    def x87(self) -> bool:
        """Get x87 CR4 Flag"""
        ...
    def __init__(self) -> None: ...
    def __int__(self) -> int: ...

class ControlRegisterFlag(Flag):
    """
    <attribute '__doc__' of 'ControlRegisterFlag' objects>
    """

    PG: ControlRegisterFlag
    """Paging R/W"""
    CD: ControlRegisterFlag
    """Cache Disable R/W"""
    NW: ControlRegisterFlag
    """Not Writethrough R/W"""
    AM: ControlRegisterFlag
    """Alignment Mask R/W"""
    WP: ControlRegisterFlag
    """Write Protect R/W"""
    NE: ControlRegisterFlag
    """Numeric Error R/W"""
    ET: ControlRegisterFlag
    """Extension Type R"""
    TS: ControlRegisterFlag
    """Task Switched R/W"""
    EM: ControlRegisterFlag
    """Emulation R/W"""
    MP: ControlRegisterFlag
    """Monitor Coprocessor R/W"""
    PE: ControlRegisterFlag
    """Protection Enabled R/W"""
    OSXSAVE: ControlRegisterFlag
    """ XSAVE and Processor Extended States Enable Bit R/W """
    FSGSBASE: ControlRegisterFlag
    """ Enable RDFSBASE, RDGSBASE, WRFSBASE, and WRGSBASE instructions R/W """
    OSXMMEXCPT: ControlRegisterFlag
    """ Operating System Unmasked Exception Support R/W """
    OSFXSR: ControlRegisterFlag
    """ Operating System FXSAVE/FXRSTOR Support R/W """
    PCE: ControlRegisterFlag
    """ Performance-Monitoring Counter Enable R/W """
    PGE: ControlRegisterFlag
    """ Page-Global Enable R/W """
    MCE: ControlRegisterFlag
    """ Machine Check Enable R/W """
    PAE: ControlRegisterFlag
    """ Physical-Address Extension R/W """
    PSE: ControlRegisterFlag
    """ Page Size Extensions R/W """
    DE: ControlRegisterFlag
    """ Debugging Extensions R/W """
    TSD: ControlRegisterFlag
    """ Time Stamp Disable R/W """
    PVI: ControlRegisterFlag
    """ Protected-Mode Virtual Interrupts R/W """
    VME: ControlRegisterFlag
    """ Virtual-8086 Mode Extensions R/W """

    def __init__(*args, **kwargs):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """
        ...

class FlagRegisterFlag(Flag):
    ID: FlagRegisterFlag
    """ID Flag R/W"""
    VIP: FlagRegisterFlag
    """Virtual Interrupt Pending R/W"""
    VIF: FlagRegisterFlag
    """Virtual Interrupt Flag R/W"""
    AC: FlagRegisterFlag
    """Alignment Check R/W"""
    VM: FlagRegisterFlag
    """Virtual-8086 Mode R/W"""
    RF: FlagRegisterFlag
    """Resume Flag R/W"""
    Reserved4: FlagRegisterFlag
    """Read as Zero"""
    NT: FlagRegisterFlag
    """Nested Task R/W"""
    IOPL2: FlagRegisterFlag
    """IOPL I/O Privilege Level R/W"""
    IOPL1: FlagRegisterFlag
    """IOPL I/O Privilege Level R/W"""
    OF: FlagRegisterFlag
    """Overflow Flag R/W"""
    DF: FlagRegisterFlag
    """Direction Flag R/W"""
    IF: FlagRegisterFlag
    """Interrupt Flag R/W"""
    TF: FlagRegisterFlag
    """Trap Flag R/W"""
    SF: FlagRegisterFlag
    """Sign Flag R/W"""
    ZF: FlagRegisterFlag
    """Zero Flag R/W"""
    Reserved3: FlagRegisterFlag
    """Read as Zero"""
    AF: FlagRegisterFlag
    """Auxiliary Flag R/W"""
    Reserved2: FlagRegisterFlag
    """Read as Zero"""
    PF: FlagRegisterFlag
    """Parity Flag R/W"""
    Reserved1: FlagRegisterFlag
    """Read as One"""
    CF: FlagRegisterFlag
    """Carry Flag R/W"""

class FlagRegister:
    @property
    def ID(self) -> bool:
        """Get ID Flag R/W"""
        ...
    @ID.setter
    def ID(self, value: bool) -> None:
        """Set ID Flag R/W"""
        ...
    @property
    def VIP(self) -> bool:
        """Get Virtual Interrupt Pending R/W"""
        ...
    @VIP.setter
    def VIP(self, value: bool) -> None:
        """Set Virtual Interrupt Pending R/W"""
        ...
    @property
    def VIF(self) -> bool:
        """Get Virtual Interrupt Flag R/W"""
        ...
    @VIF.setter
    def VIF(self, value: bool) -> None:
        """Set Virtual Interrupt Flag R/W"""
        ...
    @property
    def AC(self) -> bool:
        """Get Alignment Check R/W"""
        ...
    @AC.setter
    def AC(self, value: bool) -> None:
        """Set Alignment Check R/W"""
        ...
    @property
    def VM(self) -> bool:
        """Get Virtual-8086 Mode R/W"""
        ...
    @VM.setter
    def VM(self, value: bool) -> None:
        """Set Virtual-8086 Mode R/W"""
        ...
    @property
    def RF(self) -> bool:
        """Get Resume Flag R/W"""
        ...
    @RF.setter
    def RF(self, value: bool) -> None:
        """Set Resume Flag R/W"""
        ...
    @property
    def Reserved4(self) -> bool:
        """Get Read as Zero"""
        ...
    @property
    def NT(self) -> bool:
        """Get Nested Task R/W"""
        ...
    @NT.setter
    def NT(self, value: bool) -> None:
        """Set Nested Task R/W"""
        ...
    @property
    def IOPL(self) -> int:
        """Get IOPL I/O Privilege Level R/W"""
        ...
    @IOPL.setter
    def IOPL(self, value: int) -> None:
        """Set IOPL I/O Privilege Level R/W"""
        ...
    @property
    def OF(self) -> bool:
        """Get Overflow Flag R/W"""
        ...
    @OF.setter
    def OF(self, value: bool) -> None:
        """Set Overflow Flag R/W"""
        ...
    @property
    def DF(self) -> bool:
        """Get Direction Flag R/W"""
        ...
    @DF.setter
    def DF(self, value: bool) -> None:
        """Set Direction Flag R/W"""
        ...
    @property
    def IF(self) -> bool:
        """Get Interrupt Flag R/W"""
        ...
    @IF.setter
    def IF(self, value: bool) -> None:
        """Set Interrupt Flag R/W"""
        ...
    @property
    def TF(self) -> bool:
        """Get Trap Flag R/W"""
        ...
    @TF.setter
    def TF(self, value: bool) -> None:
        """Set Trap Flag R/W"""
        ...
    @property
    def SF(self) -> bool:
        """Get Sign Flag R/W"""
        ...
    @SF.setter
    def SF(self, value: bool) -> None:
        """Set Sign Flag R/W"""
        ...
    @property
    def ZF(self) -> bool:
        """Get Zero Flag R/W"""
        ...
    @ZF.setter
    def ZF(self, value: bool) -> None:
        """Set Zero Flag R/W"""
        ...
    @property
    def Reserved3(self) -> bool:
        """Get Read as Zero"""
        ...
    @property
    def AF(self) -> bool:
        """Get Auxiliary Flag R/W"""
        ...
    @AF.setter
    def AF(self, value: bool) -> None:
        """Set Auxiliary Flag R/W"""
        ...
    @property
    def Reserved2(self) -> bool:
        """Get Read as Zero"""
        ...
    @property
    def PF(self) -> bool:
        """Get Parity Flag R/W"""
        ...
    @PF.setter
    def PF(self, value: bool) -> None:
        """Set Parity Flag R/W"""
        ...
    @property
    def Reserved1(self) -> bool:
        """Get Read as One"""
        ...
    @property
    def CF(self) -> bool:
        """Get Carry Flag R/W"""
        ...
    @CF.setter
    def CF(self, value: bool) -> None:
        """Set Carry Flag R/W"""
        ...
    def __int__(self) -> int: ...

class FeatureRegisterFlag(Flag):
    TCE: FeatureRegisterFlag
    """Translation Cache Extension R/W"""
    FFXSR: FeatureRegisterFlag
    """Fast FXSAVE/FXRSTOR R/W"""
    LMSLE: FeatureRegisterFlag
    """Long Mode Segment Limit Enable R/W"""
    SVME: FeatureRegisterFlag
    """Secure Virtual Machine Enable R/W"""
    NXE: FeatureRegisterFlag
    """No-Execute Enable R/W"""
    LMA: FeatureRegisterFlag
    """Long Mode Active R/W"""
    LME: FeatureRegisterFlag
    """Long Mode Enable R/W"""
    SCE: FeatureRegisterFlag
    """System Call Extensions R/W"""

class FeatureRegister:
    @property
    def TCE(self) -> bool:
        """Get Translation Cache Extension R/W"""
        ...
    @TCE.setter
    def TCE(self, value: bool) -> None:
        """Set Translation Cache Extension R/W"""
        ...
    @property
    def FFXSR(self) -> bool:
        """Get Fast FXSAVE/FXRSTOR R/W"""
        ...
    @FFXSR.setter
    def FFXSR(self, value: bool) -> None:
        """Set Fast FXSAVE/FXRSTOR R/W"""
        ...
    @property
    def LMSLE(self) -> bool:
        """Get Long Mode Segment Limit Enable R/W"""
        ...
    @LMSLE.setter
    def LMSLE(self, value: bool) -> None:
        """Set Long Mode Segment Limit Enable R/W"""
        ...
    @property
    def SVME(self) -> bool:
        """Get Secure Virtual Machine Enable R/W"""
        ...
    @SVME.setter
    def SVME(self, value: bool) -> None:
        """Set Secure Virtual Machine Enable R/W"""
        ...
    @property
    def NXE(self) -> bool:
        """Get No-Execute Enable R/W"""
        ...
    @NXE.setter
    def NXE(self, value: bool) -> None:
        """Set No-Execute Enable R/W"""
        ...
    @property
    def LMA(self) -> bool:
        """Get Long Mode Active R/W"""
        ...
    @LMA.setter
    def LMA(self, value: bool) -> None:
        """Set Long Mode Active R/W"""
        ...
    @property
    def LME(self) -> bool:
        """Get Long Mode Enable R/W"""
        ...
    @LME.setter
    def LME(self, value: bool) -> None:
        """Set Long Mode Enable R/W"""
        ...
    @property
    def SCE(self) -> bool:
        """Get System Call Extensions R/W"""
        ...
    @SCE.setter
    def SCE(self, value: bool) -> None:
        """Set System Call Extensions R/W"""
        ...
    def __int__(self) -> int: ...

class ExceptionType(Enum):
    DivideError: ExceptionType
    Debug: ExceptionType
    BreakPoint: ExceptionType
    Overflow: ExceptionType
    BoundRange: ExceptionType
    InvalidOpcode: ExceptionType
    NonMaskable: ExceptionType
    DoubleFfault: ExceptionType
    InvalidTss: ExceptionType
    NotPresentSegment: ExceptionType
    Stack: ExceptionType
    GeneralProtection: ExceptionType
    PageFault: ExceptionType
    FloatingPoint: ExceptionType
    AlignmentCheck: ExceptionType
    MachineCheck: ExceptionType
    ControlProtection: ExceptionType

class Cpu:
    def __init__(*args, **kwargs):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """
        ...
    @property
    def cr2(self) -> int: ...
    @cr2.setter
    def cr2(self) -> int: ...
    @property
    def cr3(self) -> int: ...
    @cr3.setter
    def cr3(self) -> int: ...
    @property
    def cs(self) -> bochscpu._bochscpu.Segment: ...
    @cs.setter
    def cs(self) -> bochscpu._bochscpu.Segment: ...
    @property
    def ds(self) -> bochscpu._bochscpu.Segment: ...
    @ds.setter
    def ds(self) -> bochscpu._bochscpu.Segment: ...
    @property
    def es(self) -> bochscpu._bochscpu.Segment: ...
    @es.setter
    def es(self) -> bochscpu._bochscpu.Segment: ...
    @property
    def fs(self) -> bochscpu._bochscpu.Segment: ...
    @fs.setter
    def fs(self) -> bochscpu._bochscpu.Segment: ...
    @property
    def gdtr(self) -> bochscpu._bochscpu.GlobalSegment: ...
    @gdtr.setter
    def gdtr(self) -> bochscpu._bochscpu.GlobalSegment: ...
    @property
    def gs(self) -> bochscpu._bochscpu.Segment: ...
    @gs.setter
    def gs(self) -> bochscpu._bochscpu.Segment: ...
    @property
    def id(self) -> int: ...
    @property
    def idtr(self) -> bochscpu._bochscpu.GlobalSegment: ...
    @idtr.setter
    def idtr(self) -> bochscpu._bochscpu.GlobalSegment: ...
    @property
    def ldtr(self) -> bochscpu._bochscpu.Segment: ...
    @ldtr.setter
    def ldtr(self) -> bochscpu._bochscpu.Segment: ...
    @property
    def r10(self) -> int: ...
    @r10.setter
    def r10(self) -> int: ...
    @property
    def r11(self) -> int: ...
    @r11.setter
    def r11(self) -> int: ...
    @property
    def r12(self) -> int: ...
    @r12.setter
    def r12(self) -> int: ...
    @property
    def r13(self) -> int: ...
    @r13.setter
    def r13(self) -> int: ...
    @property
    def r14(self) -> int: ...
    @r14.setter
    def r14(self) -> int: ...
    @property
    def r15(self) -> int: ...
    @r15.setter
    def r15(self) -> int: ...
    @property
    def r8(self) -> int: ...
    @r8.setter
    def r8(self) -> int: ...
    @property
    def r9(self) -> int: ...
    @r9.setter
    def r9(self) -> int: ...
    @property
    def rax(self) -> int: ...
    @rax.setter
    def rax(self) -> int: ...
    @property
    def rbp(self) -> int: ...
    @rbp.setter
    def rbp(self) -> int: ...
    @property
    def rbx(self) -> int: ...
    @rbx.setter
    def rbx(self) -> int: ...
    @property
    def rcx(self) -> int: ...
    @rcx.setter
    def rcx(self) -> int: ...
    @property
    def rdi(self) -> int: ...
    @rdi.setter
    def rdi(self) -> int: ...
    @property
    def rdx(self) -> int: ...
    @rdx.setter
    def rdx(self) -> int: ...
    @property
    def rflags(self) -> int: ...
    @rflags.setter
    def rflags(self) -> int: ...
    @property
    def rip(self) -> int: ...
    @rip.setter
    def rip(self) -> int: ...
    @property
    def rsi(self) -> int: ...
    @rsi.setter
    def rsi(self) -> int: ...
    @property
    def rsp(self) -> int: ...
    @rsp.setter
    def rsp(self) -> int: ...
    def set_exception(self, vector: int, error: int) -> None: ...
    def set_mode(self) -> None: ...
    def set_state(self, state: bochscpu._bochscpu.State) -> None: ...
    def set_state_no_flush(self, state: bochscpu._bochscpu.State) -> None: ...
    @property
    def ss(self) -> bochscpu._bochscpu.Segment: ...
    @ss.setter
    def ss(self) -> bochscpu._bochscpu.Segment: ...
    @property
    def state(self) -> bochscpu._bochscpu.State: ...
    @state.setter
    def state(self) -> bochscpu._bochscpu.State: ...
    @property
    def tr(self) -> bochscpu._bochscpu.Segment: ...
    @tr.setter
    def tr(self) -> bochscpu._bochscpu.Segment: ...
    @property
    def zmm(self) -> bochscpu._bochscpu.Zmm: ...
    @zmm.setter
    def zmm(self, arg: int, /) -> bochscpu._bochscpu.Zmm: ...
