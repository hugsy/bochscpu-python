from typing import Optional
from enum import Enum

class AccessType(Enum):
    Execute: AccessType
    Read: AccessType
    Write: AccessType

class PageMapLevel4Table:
    def __init__(self) -> None:
        """
        Initiliaze the memory layout
        """
        ...
    def commit(self, pml4_pa: int, /) -> list[tuple[int, int]]:
        """
        Commit the layout of the tree to memory
        """
        ...
    def insert(self, va: int, pa: int, flags: int, /) -> None:
        """
        Associate the VA to PA
        """
        ...
    def translate(self, va: int, /) -> Optional[int]:
        """
        Translate a VA -> PA
        """
        ...

def align_address_to_page(addr: int, /) -> int:
    """
    Align an address to the page it's in
    """
    ...

def page_size() -> int:
    """
    Get the page size
    """
    ...

def allocate_host_page() -> int:
    """
    Allocate (VirtualAlloc/mmap) a page on the host, returns the HVA on success, 0 otherwise
    """
    ...

def release_host_page(hva: int) -> None:
    """
    Release (VirtualFree/munmap) a page on the host
    """
    ...

def page_insert(gpa: int, hva: int, /) -> None:
    """
    Map a GPA to a HVA in Bochs
    """
    ...

def page_remove(gpa: int) -> None:
    """
    Remove a page by its GPA
    """
    ...

def phy_read(gpa: int, size: int) -> list[int]:
    """
    Read from GPA
    """
    ...

def phy_translate(gpa: int) -> int:
    """
    Translate from GPA to HVA
    """
    ...

def phy_write(gpa: int, bytes: bytes) -> None:
    """
    Write to GPA
    """
    ...

def virt_read(cr3: int, gva: int, sz: int) -> list[int]:
    """
    Read from GVA
    """
    ...

def virt_translate(cr3: int, gva: int) -> int:
    """
    Translate from GVA to HVA
    """
    ...

def virt_write(cr3: int, gva: int, bytes: bytes) -> bool:
    """
    Write to GVA
    """
    ...
