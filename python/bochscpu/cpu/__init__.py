from bochscpu._bochscpu import State  # type: ignore

from bochscpu._bochscpu.cpu import *  # type: ignore

import bochscpu.cpu

#
# Globally using AMD Vol 2 - Figure 1-6 Operating Modes of the AMD64 Architecture
#


def set_long_mode(state: State):
    """
    Configure the CPU state to be in Long Mode. This will wipe existing value in the
    control registers

    Ref:
        AMD Vol 2 - 14.8 Long-Mode Initialization Example

    Args:
        state (State): the CPU state to set
    """
    cr0 = ControlRegister()
    cr0.PG = True  # Enable paging to activate long mode
    cr0.AM = True
    cr0.WP = True
    cr0.NE = True
    cr0.ET = True
    cr0.PE = True  # Enable protected mode

    cr4 = ControlRegister()
    cr4.PAE = True  # Enable the 64-bit page-translation-table entries

    efer = FeatureRegister()
    efer.NXE = True
    efer.LMA = True
    efer.LME = True  # Enable long mode (set EFER.LME=1).
    efer.SCE = True

    # Apply the CRs to the state
    state.cr0 = int(cr0)
    state.cr4 = int(cr4)
    state.efer = int(efer)
    return


def set_real_mode(state: State):
    """Set the CPU state to Protected Mode. CR0, CR4, and EFER will be overwritten.

    Args:
        state (State): _description_
    """
    cr0 = ControlRegister()
    cr0.PE = False

    cr4 = ControlRegister()
    cr4.PAE = False

    efer = FeatureRegister(0)
    efer.LMA = False

    state.cr0 = int(cr0)
    state.cr4 = int(cr4)
    state.efer = int(efer)
    return


def set_virtual8086_mode(state: State):
    """Set the CPU state to Protected Mode. CR0, CR4, EFER and RFLAGS will be
    overwritten.

    Args:
        state (State): _description_
    """
    cr0 = ControlRegister()
    cr0.PE = True

    cr4 = ControlRegister()
    cr4.PAE = False

    efer = FeatureRegister()
    efer.LMA = False

    rflags = FlagRegister()
    rflags.VM = True

    state.cr0 = int(cr0)
    state.cr4 = int(cr4)
    state.efer = int(efer)
    state.rflags = int(rflags)
    return


def set_protected_mode(state: State):
    """Set the CPU state to Protected Mode. CR0, CR4, EFER and RFLAGS will be
    overwritten.

    Args:
        state (State): _description_
    """
    cr0 = ControlRegister()
    cr0.PE = True

    cr4 = ControlRegister()
    cr4.PAE = False

    efer = FeatureRegister()
    efer.LMA = False

    rflags = FlagRegister()
    rflags.VM = False

    state.cr0 = int(cr0)
    state.cr4 = int(cr4)
    state.efer = int(efer)
    state.rflags = int(rflags)
    return


def is_real_mode(state: State) -> bool:
    """Indicates whether the given will run the CPU in real/legacy mode

    Args:
        state (State): the CPU state

    Returns:
        bool: True if the CPU will run in real/legacy mode
    """
    cs = SegmentFlags(state.cs.attr)
    cr0 = ControlRegister(state.cr0)
    cr4 = ControlRegister(state.cr4)
    return not cs.L and not cr0.PAE and not cr4.PG and not cr4.PGE


def is_protected_mode(state: State) -> bool:
    """Indicates whether the given will run the CPU in protected mode

    Args:
        state (State): the CPU state

    Returns:
        bool: True if the CPU will run in protected mode
    """
    cr0 = ControlRegister(state.cr0)
    cr4 = ControlRegister(state.cr4)
    efer = FeatureRegister(state.efer)
    cs = SegmentFlags(state.cs.attr)
    rflags = FlagRegister(state.rflags)
    return cr0.PE and not efer.LME and not cr4.PAE and not cs.L and not rflags.VM


def is_virtual8086_mode(state: State) -> bool:
    """Indicates whether the given will run the CPU in Virtual8086 mode

    Args:
        state (State): the CPU state

    Returns:
        bool: True if the CPU will run in Virtual8086 mode
    """
    cr0 = ControlRegister(state.cr0)
    cr4 = ControlRegister(state.cr4)
    efer = FeatureRegister(state.efer)
    cs = SegmentFlags(state.cs.attr)
    rflags = FlagRegister(state.rflags)
    return cr0.PE and not efer.LME and not cr4.PAE and not cs.L and rflags.VM


def is_long_mode(state: State) -> bool:
    """Indicates whether the given will run the CPU in long mode

    Args:
        state (State): the CPU state

    Returns:
        bool: True if the CPU will run in long mode
    """
    cr0 = ControlRegister(state.cr0)
    cr4 = ControlRegister(state.cr4)
    efer = FeatureRegister(state.efer)
    cs = SegmentFlags(state.cs.attr)
    return efer.LME and cr4.PAE and cr0.PE and cs.L
