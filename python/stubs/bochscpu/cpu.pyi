from enum import Flag
import bochscpu.cpu

class ControlRegister:
    """
    ControlRegister class
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
    def __init__(self) -> None: ...

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

class cpu:
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
    def cs(self) -> bochscpu.Segment: ...
    @cs.setter
    def cs(self) -> bochscpu.Segment: ...
    @property
    def ds(self) -> bochscpu.Segment: ...
    @ds.setter
    def ds(self) -> bochscpu.Segment: ...
    @property
    def es(self) -> bochscpu.Segment: ...
    @es.setter
    def es(self) -> bochscpu.Segment: ...
    @property
    def fs(self) -> bochscpu.Segment: ...
    @fs.setter
    def fs(self) -> bochscpu.Segment: ...
    @property
    def gdtr(self) -> bochscpu.GlobalSegment: ...
    @gdtr.setter
    def gdtr(self) -> bochscpu.GlobalSegment: ...
    @property
    def gs(self) -> bochscpu.Segment: ...
    @gs.setter
    def gs(self) -> bochscpu.Segment: ...
    @property
    def id(self) -> int: ...
    @property
    def idtr(self) -> bochscpu.GlobalSegment: ...
    @idtr.setter
    def idtr(self) -> bochscpu.GlobalSegment: ...
    @property
    def ldtr(self) -> bochscpu.Segment: ...
    @ldtr.setter
    def ldtr(self) -> bochscpu.Segment: ...
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
    def set_state_no_flush(self, state: bochscpu.State) -> None: ...
    @property
    def ss(self) -> bochscpu.Segment: ...
    @ss.setter
    def ss(self) -> bochscpu.Segment: ...
    @property
    def state(self) -> bochscpu.State: ...
    @state.setter
    def state(self) -> bochscpu.State: ...
    @property
    def tr(self) -> bochscpu.Segment: ...
    @tr.setter
    def tr(self) -> bochscpu.Segment: ...
    @property
    def zmm(self) -> bochscpu.Zmm: ...
    @zmm.setter
    def zmm(self, arg: int, /) -> bochscpu.Zmm: ...
