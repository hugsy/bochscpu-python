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
