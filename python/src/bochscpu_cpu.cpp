#include <nanobind/nanobind.h>

#include "bochscpu.hpp"

namespace nb = nanobind;
using namespace nb::literals;

///
/// @brief BochsCPU CPU submodule Python interface
///
void
bochscpu_cpu_module(nb::module_& base_module)
{
    auto m = base_module.def_submodule("cpu", "CPU module");

    nb::enum_<BochsCPU::Cpu::ControlRegisterFlag>(m, "ControlRegisterFlag")
        // cr0
        .value("PG", BochsCPU::Cpu::ControlRegisterFlag::PG, "Paging R/W")
        .value("CD", BochsCPU::Cpu::ControlRegisterFlag::CD, "Cache Disable R/W")
        .value("NW", BochsCPU::Cpu::ControlRegisterFlag::NW, "Not Writethrough R/W")
        .value("AM", BochsCPU::Cpu::ControlRegisterFlag::AM, "Alignment Mask R/W")
        .value("WP", BochsCPU::Cpu::ControlRegisterFlag::WP, "Write Protect R/W")
        .value("NE", BochsCPU::Cpu::ControlRegisterFlag::NE, "Numeric Error R/W")
        .value("ET", BochsCPU::Cpu::ControlRegisterFlag::ET, "Extension Type R")
        .value("TS", BochsCPU::Cpu::ControlRegisterFlag::TS, "Task Switched R/W")
        .value("EM", BochsCPU::Cpu::ControlRegisterFlag::EM, "Emulation R/W")
        .value("MP", BochsCPU::Cpu::ControlRegisterFlag::MP, "Monitor Coprocessor R/W")
        .value("PE", BochsCPU::Cpu::ControlRegisterFlag::PE, "Protection Enabled R/W")

        // cr4
        .value(
            "OSXSAVE",
            BochsCPU::Cpu::ControlRegisterFlag::OSXSAVE,
            "XSAVE and Processor Extended States Enable Bit R/W")
        .value(
            "FSGSBASE",
            BochsCPU::Cpu::ControlRegisterFlag::FSGSBASE,
            "Enable RDFSBASE, RDGSBASE, WRFSBASE, and WRGSBASE instructions R/W")
        .value(
            "OSXMMEXCPT",
            BochsCPU::Cpu::ControlRegisterFlag::OSXMMEXCPT,
            "Operating System Unmasked Exception Support R/W")
        .value("OSFXSR", BochsCPU::Cpu::ControlRegisterFlag::OSFXSR, "Operating System FXSAVE/FXRSTOR Support R/W")
        .value("PCE", BochsCPU::Cpu::ControlRegisterFlag::PCE, "Performance-Monitoring Counter Enable R/W")
        .value("PGE", BochsCPU::Cpu::ControlRegisterFlag::PGE, "Page-Global Enable R/W")
        .value("MCE", BochsCPU::Cpu::ControlRegisterFlag::MCE, "Machine Check Enable R/W")
        .value("PAE", BochsCPU::Cpu::ControlRegisterFlag::PAE, "Physical-Address Extension R/W")
        .value("PSE", BochsCPU::Cpu::ControlRegisterFlag::PSE, "Page Size Extensions R/W")
        .value("DE", BochsCPU::Cpu::ControlRegisterFlag::DE, "Debugging Extensions R/W")
        .value("TSD", BochsCPU::Cpu::ControlRegisterFlag::TSD, "Time Stamp Disable R/W")
        .value("PVI", BochsCPU::Cpu::ControlRegisterFlag::PVI, "Protected-Mode Virtual Interrupts R/W")
        .value("VME", BochsCPU::Cpu::ControlRegisterFlag::VME, "Virtual-8086 Mode Extensions R/W")
        .export_values();

    nb::class_<BochsCPU::Cpu::ControlRegister>(m, "ControlRegister")
        .def(nb::init<>())
        .def_prop_rw(
            "PG",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::PG);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::PG, onoff);
            })
        .def_prop_rw(
            "CD",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::CD);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::CD, onoff);
            })
        .def_prop_rw(
            "NW",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::NW);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::NW, onoff);
            })
        .def_prop_rw(
            "AM",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::AM);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::AM, onoff);
            })
        .def_prop_rw(
            "WP",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::WP);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::WP, onoff);
            })
        .def_prop_rw(
            "NE",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::NE);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::NE, onoff);
            })
        .def_prop_rw(
            "ET",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::ET);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::ET, onoff);
            })
        .def_prop_rw(
            "TS",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::TS);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::TS, onoff);
            })
        .def_prop_rw(
            "EM",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::EM);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::EM, onoff);
            })
        .def_prop_rw(
            "MP",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::MP);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::MP, onoff);
            })
        .def_prop_rw(
            "PE",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::PE);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::PE, onoff);
            })

        .def_prop_rw(
            "OSXSAVE",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::OSXSAVE);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::OSXSAVE, onoff);
            })
        .def_prop_rw(
            "FSGSBASE",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::FSGSBASE);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::FSGSBASE, onoff);
            })
        .def_prop_rw(
            "OSXMMEXCPT",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::OSXMMEXCPT);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::OSXMMEXCPT, onoff);
            })
        .def_prop_rw(
            "OSFXSR",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::OSFXSR);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::OSFXSR, onoff);
            })
        .def_prop_rw(
            "PCE",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::PCE);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::PCE, onoff);
            })
        .def_prop_rw(
            "PGE",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::PGE);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::PGE, onoff);
            })
        .def_prop_rw(
            "MCE",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::MCE);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::MCE, onoff);
            })
        .def_prop_rw(
            "PAE",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::PAE);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::PAE, onoff);
            })
        .def_prop_rw(
            "PSE",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::PSE);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::PSE, onoff);
            })
        .def_prop_rw(
            "DE",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::DE);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::DE, onoff);
            })
        .def_prop_rw(
            "TSD",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::TSD);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::TSD, onoff);
            })
        .def_prop_rw(
            "PVI",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::PVI);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::PVI, onoff);
            })
        .def_prop_rw(
            "VME",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.test((int)BochsCPU::Cpu::ControlRegisterFlag::VME);
            },
            [](BochsCPU::Cpu::ControlRegister& cr, bool onoff)
            {
                cr.set((int)BochsCPU::Cpu::ControlRegisterFlag::VME, onoff);
            })
        .def(
            "__repr__",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.to_string();
            })
        .def(
            "__int__",
            [](BochsCPU::Cpu::ControlRegister& cr)
            {
                return cr.to_ullong();
            });

    nb::class_<BochsCPU::Cpu::CPU>(m, "cpu")
        .def_ro("id", &BochsCPU::Cpu::CPU::id)

        // .def("cpu_new", &bochscpu_cpu_new, "id"_a, "Create a new CPU")
        // .def("cpu_from", &bochscpu_cpu_from, "id"_a, "Get a CPU context from a given CPU ID")
        // .def("cpu_forget", &bochscpu_cpu_forget, "cpu"_a)
        // .def("cpu_delete", &bochscpu_cpu_delete, "cpu"_a)

        .def(
            "set_mode",
            [](BochsCPU::Cpu::CPU& c)
            {
                ::bochscpu_cpu_set_mode(&c);
            })
        .def_prop_rw(
            "state",
            [](BochsCPU::Cpu::CPU& c)
            {
                State s;
                ::bochscpu_cpu_state(&c, &s);
                return s;
            },
            [](BochsCPU::Cpu::CPU& c, State& s)
            {
                ::bochscpu_cpu_set_state(&c, &s);
            })
        .def(
            "set_state_no_flush",
            [](BochsCPU::Cpu::CPU& c, State& s)
            {
                ::bochscpu_cpu_set_state_no_flush(&c, &s);
            },
            "state"_a)
        .def(
            "set_exception",
            [](BochsCPU::Cpu::CPU& c, uint32_t vector, uint32_t error)
            {
                ::bochscpu_cpu_set_exception(&c, vector, error);
            },
            "vector"_a,
            "error"_a)

        .def_prop_rw(
            "rax",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_rax(&c);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_rax(&c, v);
            })
        .def_prop_rw(
            "rcx",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_rcx(&c);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_rcx(&c, v);
            })
        .def_prop_rw(
            "rdx",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_rdx(&c);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_rdx(&c, v);
            })
        .def_prop_rw(
            "rbx",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_rbx(&c);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_rbx(&c, v);
            })
        .def_prop_rw(
            "rsp",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_rsp(&c);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_rsp(&c, v);
            })
        .def_prop_rw(
            "rbp",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_rbp(&c);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_rbp(&c, v);
            })
        .def_prop_rw(
            "rsi",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_rsi(&c);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_rsi(&c, v);
            })
        .def_prop_rw(
            "rdi",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_rdi(&c);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_rdi(&c, v);
            })
        .def_prop_rw(
            "r8",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_r8(&c);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_r8(&c, v);
            })
        .def_prop_rw(
            "r9",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_r9(&c);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_r9(&c, v);
            })
        .def_prop_rw(
            "r10",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_r10(&c);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_r10(&c, v);
            })
        .def_prop_rw(
            "r11",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_r11(&c);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_r11(&c, v);
            })
        .def_prop_rw(
            "r12",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_r12(&c);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_r12(&c, v);
            })
        .def_prop_rw(
            "r13",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_r13(&c);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_r13(&c, v);
            })
        .def_prop_rw(
            "r14",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_r14(&c);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_r14(&c, v);
            })
        .def_prop_rw(
            "r15",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_r15(&c);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_r15(&c, v);
            })
        .def_prop_rw(
            "rip",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_rip(&c);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_rip(&c, v);
            })
        .def_prop_rw(
            "rflags",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_rflags(&c);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_rflags(&c, v);
            })

        .def_prop_rw(
            "cs",
            [](BochsCPU::Cpu::CPU& c)
            {
                Seg s {};
                ::bochscpu_cpu_cs(&c, &s);
                return s;
            },
            [](BochsCPU::Cpu::CPU& c, Seg& s)
            {
                ::bochscpu_cpu_set_cs(&c, &s);
            })
        .def_prop_rw(
            "ds",
            [](BochsCPU::Cpu::CPU& c)
            {
                Seg s {};
                ::bochscpu_cpu_ds(&c, &s);
                return s;
            },
            [](BochsCPU::Cpu::CPU& c, Seg& s)
            {
                ::bochscpu_cpu_set_ds(&c, &s);
            })
        .def_prop_rw(
            "es",
            [](BochsCPU::Cpu::CPU& c)
            {
                Seg s {};
                ::bochscpu_cpu_es(&c, &s);
                return s;
            },
            [](BochsCPU::Cpu::CPU& c, Seg& s)
            {
                ::bochscpu_cpu_set_es(&c, &s);
            })
        .def_prop_rw(
            "fs",
            [](BochsCPU::Cpu::CPU& c)
            {
                Seg s {};
                ::bochscpu_cpu_fs(&c, &s);
                return s;
            },
            [](BochsCPU::Cpu::CPU& c, Seg& s)
            {
                ::bochscpu_cpu_set_fs(&c, &s);
            })
        .def_prop_rw(
            "ss",
            [](BochsCPU::Cpu::CPU& c)
            {
                Seg s {};
                ::bochscpu_cpu_ss(&c, &s);
                return s;
            },
            [](BochsCPU::Cpu::CPU& c, Seg& s)
            {
                ::bochscpu_cpu_set_ss(&c, &s);
            })
        .def_prop_rw(
            "gs",
            [](BochsCPU::Cpu::CPU& c)
            {
                Seg s {};
                ::bochscpu_cpu_gs(&c, &s);
                return s;
            },
            [](BochsCPU::Cpu::CPU& c, Seg& s)
            {
                ::bochscpu_cpu_set_gs(&c, &s);
            })
        .def_prop_rw(
            "ldtr",
            [](BochsCPU::Cpu::CPU& c)
            {
                Seg s {};
                ::bochscpu_cpu_ldtr(&c, &s);
                return s;
            },
            [](BochsCPU::Cpu::CPU& c, Seg& s)
            {
                ::bochscpu_cpu_set_ldtr(&c, &s);
            })
        .def_prop_rw(
            "tr",
            [](BochsCPU::Cpu::CPU& c)
            {
                Seg s {};
                ::bochscpu_cpu_tr(&c, &s);
                return s;
            },
            [](BochsCPU::Cpu::CPU& c, Seg& s)
            {
                ::bochscpu_cpu_set_tr(&c, &s);
            })
        .def_prop_rw(
            "gdtr",
            [](BochsCPU::Cpu::CPU& c)
            {
                GlobalSeg s {};
                ::bochscpu_cpu_gdtr(&c, &s);
                return s;
            },
            [](BochsCPU::Cpu::CPU& c, GlobalSeg& s)
            {
                ::bochscpu_cpu_set_gdtr(&c, &s);
            })
        .def_prop_rw(
            "idtr",
            [](BochsCPU::Cpu::CPU& c)
            {
                GlobalSeg s {};
                ::bochscpu_cpu_idtr(&c, &s);
                return s;
            },
            [](BochsCPU::Cpu::CPU& c, GlobalSeg& s)
            {
                ::bochscpu_cpu_set_idtr(&c, &s);
            })
        .def_prop_rw(
            "cr2",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_cr2(&c);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_cr2(&c, v);
            })
        .def_prop_rw(
            "cr3",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_cr3(&c);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_cr3(&c, v);
            })
        .def_prop_rw(
            "zmm",
            [](BochsCPU::Cpu::CPU& c, uintptr_t idx)
            {
                Zmm z {};
                ::bochscpu_cpu_zmm(&c, idx, &z);
                return z;
            },
            [](BochsCPU::Cpu::CPU& c, uintptr_t idx, Zmm& z)
            {
                ::bochscpu_cpu_set_zmm(&c, idx, &z);
            });
}