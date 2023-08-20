from typing import Any, Optional, overload
from enum import Enum
import bochscpu.memory

class AccessType(Enum):
    Execute: AccessType
    Read: AccessType
    Write: AccessType

def AlignAddressToPage(arg: int, /) -> int: ...

class PageMapLevel4Table:
    def Commit(self, arg: int, /) -> list[tuple[int, int]]:
        """
        Commit the layout of the tree to memory
        """
        ...
    def Insert(self, arg0: int, arg1: int, arg2: int, /) -> None:
        """
        Associate the VA to PA
        """
        ...
    def Translate(self, arg: int, /) -> Optional[int]:
        """
        Translate a VA -> PA
        """
        ...
    def __init__(self) -> None: ...

def PageSize() -> int: ...
def page_insert(arg0: int, arg1: int, /) -> None:
    """
    Map a GPA to a HVA
    """
    ...

def page_remove(gpa: int) -> None: ...
def phy_read(gpa: int, size: int) -> list[int]:
    """
    Read from GPA
    """
    ...

def phy_translate(gpa: int) -> int: ...
def phy_write(gpa: int, hva: bytes) -> None:
    """
    Write to GPA
    """
    ...

def virt_read(cr3: int, gva: int, sz: int) -> list[int]:
    """
    Read from GVA
    """
    ...

def virt_translate(cr3: int, gva: int) -> int: ...
def virt_write(cr3: int, gva: int, hva: bytes) -> bool:
    """
    Write to GVA
    """
    ...
