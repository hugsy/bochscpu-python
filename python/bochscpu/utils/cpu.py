from typing import Any
import bochscpu
import bochscpu.cpu


class GenericControlRegister:
    """Wrapper to easily manipulate control register"""

    # tuple(bitposition, name, descript, rw)
    FlagType = tuple[int, str, str, bool]
    bit: list[FlagType] = []
    name: str

    def __int__(self) -> int:
        return int(self.value)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        flags = ",".join([x[1] for x in self.bit if getattr(self.value, x[1])])
        return f"{self.name}({flags=})"

    def find(self, name: str) -> FlagType:
        res = [x for x in self.bit if x[1] == name]
        if len(res) != 1:
            raise IndexError(f"No index {name}")
        return res[0]

    def __getattr__(self, __name: str) -> bool:
        """Facilitate reading access to flags.

        Args:
            __name (str): _description_

        Returns:
            bool: _description_
        """
        matches = [x for x in self.bit if x[1] == __name]
        if len(matches) != 1:
            raise AttributeError
        entry = matches[0]
        return getattr(self.value, entry[1])

    def __setattr__(self, __name: str, __value: Any) -> None:
        """Facilitates direct write access to flags. Also validates access to the flag

        Args:
            __name (str): _description_
            __value (Any): _description_

        Returns:
            _type_: _description_
        """
        matches = [x for x in self.bit if x[1] == __name]
        if len(matches) != 1:
            return super().__setattr__(__name, __value)
        flag = self.find(__name)
        if flag[3] == False:
            print(f"Field '{flag[1]}' (bit {flag[0]}) is read-only")
        else:
            setattr(self.value, __name, __value)

    def __ior__(self, other: int):
        """Allow to use `|=` operator on another control register

        Args:
            other (_type_): _description_
        """
        for pos, name, _, rw in self.bit:
            if not rw:
                continue
            new_value = other & (1 << pos) != 0
            setattr(self, name, new_value)
        return self

    def __and__(self, bitpos: int) -> bool:
        return (int(self) & (1 << bitpos)) != 0


class CR0(GenericControlRegister):
    """Manipulate CR0

    Ref:
        AMD Vol2 3.1.1

    Args:
        GenericControlRegister (_type_): _description_
    """

    def __init__(self, initial_value: int):
        self.name = "CR0"
        self.value = bochscpu.cpu.ControlRegister()
        self.bit: list[GenericControlRegister.FlagType] = [
            (31, "PG", "Paging ", True),
            (30, "CD", "Cache Disable ", True),
            (29, "NW", "Not Writethrough ", True),
            (18, "AM", "Alignment Mask ", True),
            (16, "WP", "Write Protect ", True),
            (5, "NE", "Numeric Error ", True),
            (4, "ET", "Extension Type", False),
            (3, "TS", "Task Switched ", True),
            (2, "EM", "Emulation ", True),
            (1, "MP", "Monitor Coprocessor ", True),
            (0, "PE", "Protection Enabled ", True),
        ]
        if initial_value:
            self |= initial_value


class CR4(GenericControlRegister):
    """Manipulate CR4

    Ref:
        AMD Vol2 3.1.3

    Args:
        GenericControlRegister (_type_): _description_
    """

    def __init__(self, initial_value: int):
        self.name = "CR4"
        self.value = bochscpu.cpu.ControlRegister()
        self.bit: list[GenericControlRegister.FlagType] = [
            (18, "OSXSAVE", "XSAVE and Processor Extended States Enable Bit ", True),
            (
                16,
                "FSGSBASE",
                "Enable RDFSBASE/RDGSBASE/WRFSBASE/WRGSBASE instructions",
                True,
            ),
            (10, "OSXMMEXCPT", "Operating System Unmasked Exception Support ", True),
            (9, "OSFXSR", "Operating System FXSAVE/FXRSTOR Support ", True),
            (8, "PCE", "Performance-Monitoring Counter Enable ", True),
            (7, "PGE", "Page-Global Enable ", True),
            (6, "MCE", "Machine Check Enable ", True),
            (5, "PAE", "Physical-Address Extension ", True),
            (4, "PSE", "Page Size Extensions ", True),
            (3, "DE", "Debugging Extensions ", True),
            (2, "TSD", "Time Stamp Disable ", True),
            (1, "PVI", "Protected-Mode Virtual Interrupts ", True),
            (0, "VME", "Virtual-8086 Mode Extensions ", True),
        ]
        if initial_value:
            self |= initial_value


class EFER(GenericControlRegister):
    """Manipulate EFER

    Ref:
        AMD Vol2 3.1.7

    Args:
        GenericControlRegister (_type_): _description_
    """

    def __init__(self, initial_value: int):
        self.name = "EFER"
        self.value = bochscpu.cpu.FeatureRegister()
        self.bit: list[GenericControlRegister.FlagType] = [
            (15, "TCE", "Translation Cache Extension", True),
            (14, "FFXSR", "Fast FXSAVE/FXRSTOR", True),
            (13, "LMSLE", "Long Mode Segment Limit Enable", True),
            (12, "SVME", "Secure Virtual Machine Enable", True),
            (11, "NXE", "No-Execute Enable", True),
            (10, "LMA", "Long Mode Active", True),
            (8, "LME", "Long Mode Enable", True),
            (0, "SCE", "System Call Extensions", True),
        ]
        if initial_value:
            self |= initial_value


class RFLAGS(GenericControlRegister):
    """Manipulate RFLAGS

    Ref:
        AMD Vol2 3.1.6

    Args:
        GenericControlRegister (_type_): _description_
    """

    def __init__(self, initial_value: int):
        self.name = "RFLAGS"
        self.value = bochscpu.cpu.FlagRegister()
        self.bit: list[GenericControlRegister.FlagType] = [
            (21, "ID", "ID Flag", True),
            (20, "VIP", "Virtual Interrupt Pending", True),
            (19, "VIF", "Virtual Interrupt Flag", True),
            (18, "AC", "Alignment Check", True),
            (17, "VM", "Virtual-8086 Mode", True),
            (16, "RF", "Resume Flag", True),
            (14, "NT", "Nested Task", True),
            (13, "IOPL1", "IOPL I/O Privilege Level - High", True),
            (12, "IOPL0", "IOPL I/O Privilege Level - Low", True),
            (11, "OF", "Overflow Flag", True),
            (10, "DF", "Direction Flag", True),
            (9, "IF", "Interrupt Flag", True),
            (8, "TF", "Trap Flag", True),
            (7, "SF", "Sign Flag", True),
            (6, "ZF", "Zero Flag", True),
            (4, "AF", "Auxiliary Flag", True),
            (2, "PF", "Parity Flag", True),
            (1, "Reserved1", "Reserved, Read as One", True),
            (0, "CF", "Carry Flag", True),
        ]
        if initial_value:
            self |= initial_value


class XCR0(GenericControlRegister):
    """Manipulate XCR0

    Ref:
        AMD Vol2 11.5.2

    Args:
        GenericControlRegister (_type_): _description_
    """

    def __init__(self, initial_value: int):
        self.name = "XCR0"
        self.value = bochscpu.cpu.ControlRegister()
        self.bit: list[GenericControlRegister.FlagType] = [
            (63, "X", "Reserved specifically for XCR0 bit vector expansion.", False),
            (
                62,
                "LWP",
                "When set, Lightweight Profiling (LWP) extensions are enabled and XSAVE/XRSTOR supports LWP state management.",
                True,
            ),
            (
                2,
                "YMM",
                "When set, 256-bit SSE state management is supported by XSAVE/XRSTOR. Must be set to enable AVX extensions",
                True,
            ),
            (
                1,
                "SSE",
                "When set, 128-bit SSE state management is supported by XSAVE/XRSTOR. This bit must be set if YMM is set. Must be set to enable AVX extensions.",
                True,
            ),
            (
                0,
                "x87",
                "x87 FPU state management is supported by XSAVE/XRSTOR. Must be set to 1.",
                False,
            ),
        ]
        if initial_value:
            self |= initial_value
