#include <nanobind/nanobind.h>
#include <nanobind/operators.h>
#include <nanobind/stl/string.h>

#include <sstream>

#include "bochscpu.hpp"

namespace nb = nanobind;
using namespace nb::literals;

#define GenericGetterSetterStatic(cls, name, enum_cls, desc, value)                                                    \
    def_prop_rw(                                                                                                       \
        #name,                                                                                                         \
        [](cls const& x)                                                                                               \
        {                                                                                                              \
            return x.test((int)enum_cls::name);                                                                        \
        },                                                                                                             \
        [](cls& x, bool b)                                                                                             \
        {                                                                                                              \
            x.set((int)enum_cls::name, value);                                                                         \
        },                                                                                                             \
        desc)

#define GenericGetterSetter(cls, name, enum_cls, desc)                                                                 \
    def_prop_rw(                                                                                                       \
        #name,                                                                                                         \
        [](cls const& x)                                                                                               \
        {                                                                                                              \
            return x.test((int)enum_cls::name);                                                                        \
        },                                                                                                             \
        [](cls& x, bool b)                                                                                             \
        {                                                                                                              \
            x.set((int)enum_cls::name, b);                                                                             \
        },                                                                                                             \
        desc)


///
/// @brief BochsCPU CPU submodule Python interface
///
void
bochscpu_cpu_module(nb::module_& base_module)
{
    auto m = base_module.def_submodule("cpu", "CPU module");

#pragma region ControlRegister
    nb::enum_<BochsCPU::Cpu::ControlRegisterFlag>(m, "ControlRegisterFlag")
        // clang-format off
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
        .value("OSXSAVE", BochsCPU::Cpu::ControlRegisterFlag::OSXSAVE, "XSAVE and Processor Extended States Enable Bit R/W")
        .value("FSGSBASE", BochsCPU::Cpu::ControlRegisterFlag::FSGSBASE, "Enable RDFSBASE, RDGSBASE, WRFSBASE, and WRGSBASE instructions R/W")
        .value("OSXMMEXCPT",BochsCPU::Cpu::ControlRegisterFlag::OSXMMEXCPT,"Operating System Unmasked Exception Support R/W")
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

        // xcr0
        .value("X", BochsCPU::Cpu::ControlRegisterFlag::X, "Reserved specifically for XCR0 bit vector expansion. ")
        .value("LWP", BochsCPU::Cpu::ControlRegisterFlag::LWP, "When set, Lightweight Profiling (LWP) extensions are enabled and XSAVE/XRSTOR supports LWP state management.")
        .value("YMM", BochsCPU::Cpu::ControlRegisterFlag::YMM,"When set, 256-bit SSE state management is supported by XSAVE/XRSTOR. Must be set to enable AVX extensions.")
        .value("SSE",BochsCPU::Cpu::ControlRegisterFlag::SSE,"When set, 128-bit SSE state management is supported by XSAVE/XRSTOR. This bit must be set if YMM is set. Must be set to enable AVX extensions.")
        .value("x87", BochsCPU::Cpu::ControlRegisterFlag::x87,"x87 FPU state management is supported by XSAVE/XRSTOR. Must be set to 1.")
        // clang-format on
        .export_values();


#define GetterSetter(name, desc)                                                                                       \
    GenericGetterSetter(BochsCPU::Cpu::ControlRegister, name, BochsCPU::Cpu::ControlRegisterFlag, desc)

    nb::class_<BochsCPU::Cpu::ControlRegister>(m, "ControlRegister")
        .def(nb::init<>())
        .def(nb::init<uint64_t>())

        // cr0
        .GetterSetter(PG, "Paging R/W")
        .GetterSetter(CD, "Cache Disable R/W")
        .GetterSetter(NW, "Not Writethrough R/W")
        .GetterSetter(AM, "Alignment Mask R/W")
        .GetterSetter(WP, "Write Protect R/W")
        .GetterSetter(NE, "Numeric Error R/W")
        .GetterSetter(ET, "Extension Type R")
        .GetterSetter(TS, "Task Switched R/W")
        .GetterSetter(EM, "Emulation R/W")
        .GetterSetter(MP, "Monitor Coprocessor R/W")
        .GetterSetter(PE, "Protection Enabled R/W")

        // cr4
        .GetterSetter(OSXSAVE, "XSAVE and Processor Extended States Enable Bit R/W")
        .GetterSetter(FSGSBASE, "Enable RDFSBASE, RDGSBASE, WRFSBASE, and WRGSBASE instructions R/W")
        .GetterSetter(OSXMMEXCPT, "Operating System Unmasked Exception Support R/W")
        .GetterSetter(OSFXSR, "Operating System FXSAVE/FXRSTOR Support R/W")
        .GetterSetter(PCE, "Performance-Monitoring Counter Enable R/W")
        .GetterSetter(PGE, "Page-Global Enable R/W")
        .GetterSetter(MCE, "Machine Check Enable R/W")
        .GetterSetter(PAE, "Physical-Address Extension R/W")
        .GetterSetter(PSE, "Page Size Extensions R/W")
        .GetterSetter(DE, "Debugging Extensions R/W")
        .GetterSetter(TSD, "Time Stamp Disable R/W")
        .GetterSetter(PVI, "Protected-Mode Virtual Interrupts R/W")
        .GetterSetter(VME, "Virtual-8086 Mode Extensions R/W")

        // xcr0
        .GetterSetter(X, "Reserved specifically for XCR0 bit vector expansion. ")
        .GetterSetter(
            LWP,
            "When set, Lightweight Profiling (LWP) extensions are enabled and XSAVE/XRSTOR supports LWP state "
            "management.")
        .GetterSetter(
            YMM,
            "When set, 256-bit SSE state management is supported by XSAVE/XRSTOR. Must be set to enable AVX "
            "extensions.")
        .GetterSetter(
            SSE,
            "When set, 128-bit SSE state management is supported by XSAVE/XRSTOR. This bit must be set if YMM is set. "
            "Must be set to enable AVX extensions.")
        .GetterSetter(x87, "x87 FPU state management is supported by XSAVE/XRSTOR. Must be set to 1.")

        .def(
            "__repr__",
            [](BochsCPU::Cpu::ControlRegister const& x)
            {
                return x.to_string();
            })
        .def(
            "__str__",
            [](BochsCPU::Cpu::ControlRegister const& x)
            {
                return x.to_string();
            })
        .def(
            "cr0_str",
            [](BochsCPU::Cpu::ControlRegister const& x)
            {
                std::stringstream ss;
                ss << "[ ";
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::PG) ? "PG " : "pg ");
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::CD) ? "CD " : "cd ");
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::NW) ? "NW " : "nw ");
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::AM) ? "AM " : "am ");
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::WP) ? "WP " : "wp ");
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::NE) ? "NE " : "ne ");
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::ET) ? "ET " : "et ");
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::TS) ? "TS " : "ts ");
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::EM) ? "EM " : "em ");
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::MP) ? "MP " : "mp ");
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::PE) ? "PE " : "pe ");
                ss << "]";
                return ss.str();
            })
        .def(
            "cr4_str",
            [](BochsCPU::Cpu::ControlRegister const& x)
            {
                std::stringstream ss;
                ss << "[ ";
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::OSXSAVE) ? "OSXSAVE " : "osxsave ");
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::FSGSBASE) ? "FSGSBASE " : "fsgsbase ");
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::OSXMMEXCPT) ? "OSXMMEXCPT " : "osxmmexcpt ");
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::OSFXSR) ? "OSFXSR " : "osfxsr ");
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::PCE) ? "PCE " : "pce ");
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::PGE) ? "PGE " : "pge ");
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::MCE) ? "MCE " : "mce ");
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::PAE) ? "PAE " : "pae ");
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::PSE) ? "PSE " : "pse ");
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::DE) ? "DE " : "de ");
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::TSD) ? "TSD " : "tsd ");
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::PVI) ? "PVI " : "pvi ");
                ss << (x.test((int)BochsCPU::Cpu::ControlRegisterFlag::VME) ? "VME " : "vme ");
                ss << "]";
                return ss.str();
            })
        .def(
            "__int__",
            [](BochsCPU::Cpu::ControlRegister const& x)
            {
                return x.to_ullong();
            });
#undef GetterSetter

#pragma endregion

#pragma region FlagRegister
    nb::enum_<BochsCPU::Cpu::FlagRegisterFlag>(m, "FlagRegisterFlag")
        .value("ID", BochsCPU::Cpu::FlagRegisterFlag::ID, "ID Flag R/W")
        .value("VIP", BochsCPU::Cpu::FlagRegisterFlag::VIP, "Virtual Interrupt Pending R/W")
        .value("VIF", BochsCPU::Cpu::FlagRegisterFlag::VIF, "Virtual Interrupt Flag R/W")
        .value("AC", BochsCPU::Cpu::FlagRegisterFlag::AC, "Alignment Check R/W")
        .value("VM", BochsCPU::Cpu::FlagRegisterFlag::VM, "Virtual-8086 Mode R/W")
        .value("RF", BochsCPU::Cpu::FlagRegisterFlag::RF, "Resume Flag R/W")
        .value("Reserved4", BochsCPU::Cpu::FlagRegisterFlag::Reserved4, "Read as Zero")
        .value("NT", BochsCPU::Cpu::FlagRegisterFlag::NT, "Nested Task R/W")
        .value("IOPL2", BochsCPU::Cpu::FlagRegisterFlag::IOPL2, "IOPL I/O Privilege Level R/W")
        .value("IOPL1", BochsCPU::Cpu::FlagRegisterFlag::IOPL1, "IOPL I/O Privilege Level R/W")
        .value("OF", BochsCPU::Cpu::FlagRegisterFlag::OF, "Overflow Flag R/W")
        .value("DF", BochsCPU::Cpu::FlagRegisterFlag::DF, "Direction Flag R/W")
        .value("IF", BochsCPU::Cpu::FlagRegisterFlag::IF, "Interrupt Flag R/W")
        .value("TF", BochsCPU::Cpu::FlagRegisterFlag::TF, "Trap Flag R/W")
        .value("SF", BochsCPU::Cpu::FlagRegisterFlag::SF, "Sign Flag R/W")
        .value("ZF", BochsCPU::Cpu::FlagRegisterFlag::ZF, "Zero Flag R/W")
        .value("Reserved3", BochsCPU::Cpu::FlagRegisterFlag::Reserved3, "Read as Zero")
        .value("AF", BochsCPU::Cpu::FlagRegisterFlag::AF, "Auxiliary Flag R/W")
        .value("Reserved2", BochsCPU::Cpu::FlagRegisterFlag::Reserved2, "Read as Zero")
        .value("PF", BochsCPU::Cpu::FlagRegisterFlag::PF, "Parity Flag R/W")
        .value("Reserved1", BochsCPU::Cpu::FlagRegisterFlag::Reserved1, "Read as One")
        .value("CF", BochsCPU::Cpu::FlagRegisterFlag::CF, "Carry Flag R/W")
        .export_values();

#define GetterSetter(name, desc)                                                                                       \
    GenericGetterSetter(BochsCPU::Cpu::FlagRegister, name, BochsCPU::Cpu::FlagRegisterFlag, desc)

#define GetterSetterStatic(name, desc, val)                                                                            \
    GenericGetterSetterStatic(BochsCPU::Cpu::FlagRegister, name, BochsCPU::Cpu::FlagRegisterFlag, desc, val)

    nb::class_<BochsCPU::Cpu::FlagRegister>(m, "FlagRegister")
        .def(nb::init<>())
        .def(nb::init<uint64_t>())
        .GetterSetter(ID, "ID Flag R/W")
        .GetterSetter(VIP, "Virtual Interrupt Pending R/W")
        .GetterSetter(VIF, "Virtual Interrupt Flag R/W")
        .GetterSetter(AC, "Alignment Check R/W")
        .GetterSetter(VM, "Virtual-8086 Mode R/W")
        .GetterSetter(RF, "Resume Flag R/W")
        .GetterSetterStatic(Reserved4, "Read as Zero", false)
        .GetterSetter(NT, "Nested Task R/W")
        .GetterSetter(OF, "Overflow Flag R/W")
        .GetterSetter(DF, "Direction Flag R/W")
        .GetterSetter(IF, "Interrupt Flag R/W")
        .GetterSetter(TF, "Trap Flag R/W")
        .GetterSetter(SF, "Sign Flag R/W")
        .GetterSetter(ZF, "Zero Flag R/W")
        .GetterSetterStatic(Reserved3, "Read as Zero", false)
        .GetterSetter(AF, "Auxiliary Flag R/W")
        .GetterSetterStatic(Reserved2, "Read as Zero", false)
        .GetterSetter(PF, "Parity Flag R/W")
        .GetterSetterStatic(Reserved1, "Read as One", true)
        .GetterSetter(CF, "Carry Flag R/W")

        .def_prop_rw(
            "IOPL",
            [](BochsCPU::Cpu::FlagRegister& fr)
            {
                return int(fr.test((int)BochsCPU::Cpu::FlagRegisterFlag::IOPL2)) << 1 |
                       int(fr.test((int)BochsCPU::Cpu::FlagRegisterFlag::IOPL1)) << 0;
            },
            [](BochsCPU::Cpu::FlagRegister& fr, uint8_t iopl)
            {
                fr.set((int)BochsCPU::Cpu::FlagRegisterFlag::IOPL2, iopl & 2);
                fr.set((int)BochsCPU::Cpu::FlagRegisterFlag::IOPL1, iopl & 1);
            },
            "IOPL I/O Privilege Level R/W")
        .def(
            "__repr__",
            [](BochsCPU::Cpu::FlagRegister const& x)
            {
                return x.to_string();
            })
        .def(
            "__str__",
            [](BochsCPU::Cpu::FlagRegister const& x)
            {
                std::stringstream ss;
                ss << "[ ";
                ss << (x.test((int)BochsCPU::Cpu::FlagRegisterFlag::ID) ? "ID " : "id ");
                ss << (x.test((int)BochsCPU::Cpu::FlagRegisterFlag::VIP) ? "VIP " : "vip ");
                ss << (x.test((int)BochsCPU::Cpu::FlagRegisterFlag::VIF) ? "VIF " : "vif ");
                ss << (x.test((int)BochsCPU::Cpu::FlagRegisterFlag::AC) ? "AC " : "ac ");
                ss << (x.test((int)BochsCPU::Cpu::FlagRegisterFlag::VM) ? "VM " : "vm ");
                ss << (x.test((int)BochsCPU::Cpu::FlagRegisterFlag::RF) ? "RF " : "rf ");
                // ss << (x.test((int)BochsCPU::Cpu::FlagRegisterFlag::Reserved4) ? "Reserved4 " : "reserved4 ");
                ss << (x.test((int)BochsCPU::Cpu::FlagRegisterFlag::NT) ? "NT " : "nt ");
                ss << (x.test((int)BochsCPU::Cpu::FlagRegisterFlag::OF) ? "OF " : "of ");
                ss << (x.test((int)BochsCPU::Cpu::FlagRegisterFlag::DF) ? "DF " : "df ");
                ss << (x.test((int)BochsCPU::Cpu::FlagRegisterFlag::IF) ? "IF " : "if ");
                ss << (x.test((int)BochsCPU::Cpu::FlagRegisterFlag::TF) ? "TF " : "tf ");
                ss << (x.test((int)BochsCPU::Cpu::FlagRegisterFlag::SF) ? "SF " : "sf ");
                ss << (x.test((int)BochsCPU::Cpu::FlagRegisterFlag::ZF) ? "ZF " : "zf ");
                // ss << (x.test((int)BochsCPU::Cpu::FlagRegisterFlag::Reserved3) ? "Reserved3 " : "reserved3 ");
                ss << (x.test((int)BochsCPU::Cpu::FlagRegisterFlag::AF) ? "AF " : "af ");
                // ss << (x.test((int)BochsCPU::Cpu::FlagRegisterFlag::Reserved2) ? "Reserved2 " : "reserved2 ");
                ss << (x.test((int)BochsCPU::Cpu::FlagRegisterFlag::PF) ? "PF " : "pf ");
                // ss << (x.test((int)BochsCPU::Cpu::FlagRegisterFlag::Reserved1) ? "Reserved1 " : "reserved1 ");
                ss << (x.test((int)BochsCPU::Cpu::FlagRegisterFlag::CF) ? "CF " : "cf ");
                ss << " ]";
                return ss.str();
            })
        .def(
            "__int__",
            [](BochsCPU::Cpu::FlagRegister const& x)
            {
                return x.to_ullong();
            });
#undef GetterSetter
#undef GetterSetterStatic

#pragma endregion

#pragma region FeatureRegister

    nb::enum_<BochsCPU::Cpu::FeatureRegisterFlag>(m, "FeatureRegisterFlag")
        .value("TCE", BochsCPU::Cpu::FeatureRegisterFlag::TCE, "Translation Cache Extension R/W")
        .value("FFXSR", BochsCPU::Cpu::FeatureRegisterFlag::FFXSR, "Fast FXSAVE/FXRSTOR R/W")
        .value("LMSLE", BochsCPU::Cpu::FeatureRegisterFlag::LMSLE, "Long Mode Segment Limit Enable R/W")
        .value("SVME", BochsCPU::Cpu::FeatureRegisterFlag::SVME, "Secure Virtual Machine Enable R/W")
        .value("NXE", BochsCPU::Cpu::FeatureRegisterFlag::NXE, "No-Execute Enable R/W")
        .value("LMA", BochsCPU::Cpu::FeatureRegisterFlag::LMA, "Long Mode Active R/W")
        .value("LME", BochsCPU::Cpu::FeatureRegisterFlag::LME, "Long Mode Enable R/W")
        .value("SCE", BochsCPU::Cpu::FeatureRegisterFlag::SCE, "System Call Extensions R/W")
        .export_values();


#define GetterSetter(name, desc)                                                                                       \
    GenericGetterSetter(BochsCPU::Cpu::FeatureRegister, name, BochsCPU::Cpu::FeatureRegisterFlag, desc)

    nb::class_<BochsCPU::Cpu::FeatureRegister>(m, "FeatureRegister")
        .def(nb::init<>())
        .def(nb::init<uint64_t>())
        .GetterSetter(TCE, "Translation Cache Extension R/W")
        .GetterSetter(FFXSR, "Fast FXSAVE/FXRSTOR R/W")
        .GetterSetter(LMSLE, "Long Mode Segment Limit Enable R/W")
        .GetterSetter(SVME, "Secure Virtual Machine Enable R/W")
        .GetterSetter(NXE, "No-Execute Enable R/W")
        .GetterSetter(LMA, "Long Mode Active R/W")
        .GetterSetter(LME, "Long Mode Enable R/W")
        .GetterSetter(SCE, "System Call Extensions R/W")
        .def(
            "__repr__",
            [](BochsCPU::Cpu::FeatureRegister const& x)
            {
                return x.to_string();
            })
        .def(
            "__str__",
            [](BochsCPU::Cpu::FeatureRegister const& x)
            {
                std::stringstream ss;
                ss << "[ ";
                ss << (x.test((int)BochsCPU::Cpu::FeatureRegisterFlag::TCE) ? "TCE " : "tce ");
                ss << (x.test((int)BochsCPU::Cpu::FeatureRegisterFlag::FFXSR) ? "FFXSR " : "ffxsr ");
                ss << (x.test((int)BochsCPU::Cpu::FeatureRegisterFlag::LMSLE) ? "LMSLE " : "lmsle ");
                ss << (x.test((int)BochsCPU::Cpu::FeatureRegisterFlag::SVME) ? "SVME " : "svme ");
                ss << (x.test((int)BochsCPU::Cpu::FeatureRegisterFlag::NXE) ? "NXE " : "nxe ");
                ss << (x.test((int)BochsCPU::Cpu::FeatureRegisterFlag::LMA) ? "LMA " : "lma ");
                ss << (x.test((int)BochsCPU::Cpu::FeatureRegisterFlag::LME) ? "LME " : "lme ");
                ss << (x.test((int)BochsCPU::Cpu::FeatureRegisterFlag::SCE) ? "SCE " : "sce ");
                ss << " ]";
                return ss.str();
            })
        .def(
            "__int__",
            [](BochsCPU::Cpu::FeatureRegister const& x)
            {
                return x.to_ullong();
            });
#undef GetterSetter

#pragma endregion

#pragma region SegmentRegister

    nb::enum_<BochsCPU::Cpu::SegmentRegisterFlag>(m, "SegmentRegisterFlag")
        .value("RPL0", BochsCPU::Cpu::SegmentRegisterFlag::RPL0, "Low-bit for Requested Privilege Level")
        .value("RPL1", BochsCPU::Cpu::SegmentRegisterFlag::RPL1, "High-bit for Requested Privilege Level")
        .export_values();

    nb::enum_<BochsCPU::Cpu::SegmentFlag>(m, "SegmentFlag")
        .value("A", BochsCPU::Cpu::SegmentFlag::A, "Accessed")
        .value("R", BochsCPU::Cpu::SegmentFlag::R, "Readable - CS only")
        .value("W", BochsCPU::Cpu::SegmentFlag::W, "Writable - DS/ES/FS/SS only")
        .value("C", BochsCPU::Cpu::SegmentFlag::C, "Conforming")
        .value("D", BochsCPU::Cpu::SegmentFlag::D, "Expand-down (Data)")
        .value("E", BochsCPU::Cpu::SegmentFlag::E, "Executable - CS only (1) else (0)")
        .value("S", BochsCPU::Cpu::SegmentFlag::S, "SegmentType - CS/SS only (1)")
        .value("DPL0", BochsCPU::Cpu::SegmentFlag::DPL0, "Low-bit for Descriptor Privilege Level")
        .value("DPL1", BochsCPU::Cpu::SegmentFlag::DPL1, "High-bit for Descriptor Privilege Level")
        .value("P", BochsCPU::Cpu::SegmentFlag::P, "Present")
        .value("AVL", BochsCPU::Cpu::SegmentFlag::AVL, "Available bit")
        .value("L", BochsCPU::Cpu::SegmentFlag::L, "Long bit - CS only")
        .value("DB", BochsCPU::Cpu::SegmentFlag::DB, "(32b) Default-Operand Size (D) Bit - CS only (1)")
        .value("G", BochsCPU::Cpu::SegmentFlag::G, "Granularity (G) Bit - CS only")
        .export_values();

#define GetterSetter(name, desc)                                                                                       \
    GenericGetterSetter(BochsCPU::Cpu::SegmentFlags, name, BochsCPU::Cpu::SegmentFlag, desc)

    nb::class_<BochsCPU::Cpu::SegmentFlags>(m, "SegmentFlags")
        .def(nb::init<>())
        .def(nb::init<uint16_t>())
        .GetterSetter(A, "Accessed bit")
        .GetterSetter(R, "Readable bit - CS only")
        .GetterSetter(W, "Writable bit - DS/ES/FS/SS only")
        .GetterSetter(C, "Conforming bit")
        .GetterSetter(D, "Expand-down (Data)")
        .GetterSetter(E, "Executable bit - CS only (1) otherwise (0)")
        .GetterSetter(S, "SegmentType bit - CS/SS only (1)")
        .GetterSetter(P, "Present bit")
        .GetterSetter(AVL, "Available bit")
        .GetterSetter(L, "Long bit - CS only")
        .GetterSetter(DB, "(32b) Default-Operand Size (D) Bit - CS only (1)")
        .GetterSetter(G, "Granularity (G) Bit - CS only")

        .def_prop_rw(
            "DPL",
            [](BochsCPU::Cpu::SegmentFlags& x)
            {
                return int(x.test((int)BochsCPU::Cpu::SegmentFlag::DPL1)) << 1 |
                       int(x.test((int)BochsCPU::Cpu::SegmentFlag::DPL0)) << 0;
            },
            [](BochsCPU::Cpu::SegmentFlags& x, uint8_t dpl)
            {
                x.set((int)BochsCPU::Cpu::SegmentFlag::DPL1, dpl & 2);
                x.set((int)BochsCPU::Cpu::SegmentFlag::DPL0, dpl & 1);
            },
            "IOPL I/O Privilege Level R/W")

        .def(
            "__repr__",
            [](BochsCPU::Cpu::SegmentFlags const& x)
            {
                return x.to_string();
            })
        .def(
            "__str__",
            [](BochsCPU::Cpu::SegmentFlags const& x)
            {
                std::ostringstream ss;
                ss << "SegmentFlags(";
                // clang-format off
                if ( x.test((int)BochsCPU::Cpu::SegmentFlag::G) )   ss << " G";
                if ( x.test((int)BochsCPU::Cpu::SegmentFlag::DB) )  ss << " DB";
                if ( x.test((int)BochsCPU::Cpu::SegmentFlag::AVL) ) ss << " AVL";
                if ( x.test((int)BochsCPU::Cpu::SegmentFlag::L) )   ss << " L";
                if ( x.test((int)BochsCPU::Cpu::SegmentFlag::P) )   ss << " P";
                if ( x.test((int)BochsCPU::Cpu::SegmentFlag::S) )   ss << " S";
                if ( x.test((int)BochsCPU::Cpu::SegmentFlag::E) )   ss << " E";
                if ( x.test((int)BochsCPU::Cpu::SegmentFlag::C) )   ss << " C";
                if ( x.test((int)BochsCPU::Cpu::SegmentFlag::W) )   ss << " W";
                if ( x.test((int)BochsCPU::Cpu::SegmentFlag::R) )   ss << " R";
                if ( x.test((int)BochsCPU::Cpu::SegmentFlag::A) )   ss << " A";
                // clang-format on
                ss << " )";
                return ss.str();
            })
        .def(
            "__int__",
            [](BochsCPU::Cpu::SegmentFlags const& x)
            {
                return x.to_ullong();
            });
#undef GetterSetter

#pragma endregion

#pragma region CPU Exceptions
    ///
    /// @brief AMD Manual Vol 2 - 8.1
    ///
    ///
    nb::enum_<BochsCPU::BochsException>(m, "ExceptionType", "CPU Exceptions")
        .value("DivideError", BochsCPU::BochsException::BX_DE_EXCEPTION)
        .value("Debug", BochsCPU::BochsException::BX_DB_EXCEPTION)
        .value("BreakPoint", BochsCPU::BochsException::BX_BP_EXCEPTION)
        .value("Overflow", BochsCPU::BochsException::BX_OF_EXCEPTION)
        .value("BoundRange", BochsCPU::BochsException::BX_BR_EXCEPTION)
        .value("InvalidOpcode", BochsCPU::BochsException::BX_UD_EXCEPTION)
        .value("NonMaskable", BochsCPU::BochsException::BX_NM_EXCEPTION)
        .value("DoubleFfault", BochsCPU::BochsException::BX_DF_EXCEPTION)
        .value("InvalidTss", BochsCPU::BochsException::BX_TS_EXCEPTION)
        .value("NotPresentSegment", BochsCPU::BochsException::BX_NP_EXCEPTION)
        .value("Stack", BochsCPU::BochsException::BX_SS_EXCEPTION)
        .value("GeneralProtection", BochsCPU::BochsException::BX_GP_EXCEPTION)
        .value("PageFault", BochsCPU::BochsException::BX_PF_EXCEPTION)
        .value("FloatingPoint", BochsCPU::BochsException::BX_MF_EXCEPTION)
        .value("AlignmentCheck", BochsCPU::BochsException::BX_AC_EXCEPTION)
        .value("MachineCheck", BochsCPU::BochsException::BX_MC_EXCEPTION)
        .value("ControlProtection", BochsCPU::BochsException::BX_CP_EXCEPTION)
        .export_values();
#pragma endregion

#pragma region CPU class
    nb::class_<BochsCPU::Cpu::CPU>(m, "Cpu")
        .def_ro("id", &BochsCPU::Cpu::CPU::id)
        .def(
            "set_mode",
            [](BochsCPU::Cpu::CPU& c)
            {
                ::bochscpu_cpu_set_mode(c.__cpu);
            })
        .def_prop_rw(
            "state",
            [](BochsCPU::Cpu::CPU& c)
            {
                State s {};
                ::bochscpu_cpu_state(c.__cpu, &s);
                return s;
            },
            [](BochsCPU::Cpu::CPU& c, State& s)
            {
                ::bochscpu_cpu_set_state(c.__cpu, &s);
            })
        .def(
            "set_state_no_flush",
            [](BochsCPU::Cpu::CPU& c, State& s)
            {
                ::bochscpu_cpu_set_state_no_flush(c.__cpu, &s);
            },
            "state"_a)
        .def(
            "set_state",
            [](BochsCPU::Cpu::CPU& c, State& s)
            {
                ::bochscpu_cpu_set_state(c.__cpu, &s);
            },
            "state"_a)
        .def(
            "set_exception",
            [](BochsCPU::Cpu::CPU& c, uint32_t vector, uint32_t error)
            {
                ::bochscpu_cpu_set_exception(c.__cpu, vector, error);
            },
            "vector"_a,
            "error"_a)
        .def_prop_rw(
            "rax",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_rax(c.__cpu);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_rax(c.__cpu, v);
            })
        .def_prop_rw(
            "rcx",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_rcx(c.__cpu);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_rcx(c.__cpu, v);
            })
        .def_prop_rw(
            "rdx",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_rdx(c.__cpu);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_rdx(c.__cpu, v);
            })
        .def_prop_rw(
            "rbx",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_rbx(c.__cpu);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_rbx(c.__cpu, v);
            })
        .def_prop_rw(
            "rsp",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_rsp(c.__cpu);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_rsp(c.__cpu, v);
            })
        .def_prop_rw(
            "rbp",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_rbp(c.__cpu);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_rbp(c.__cpu, v);
            })
        .def_prop_rw(
            "rsi",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_rsi(c.__cpu);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_rsi(c.__cpu, v);
            })
        .def_prop_rw(
            "rdi",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_rdi(c.__cpu);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_rdi(c.__cpu, v);
            })
        .def_prop_rw(
            "r8",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_r8(c.__cpu);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_r8(c.__cpu, v);
            })
        .def_prop_rw(
            "r9",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_r9(c.__cpu);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_r9(c.__cpu, v);
            })
        .def_prop_rw(
            "r10",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_r10(c.__cpu);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_r10(c.__cpu, v);
            })
        .def_prop_rw(
            "r11",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_r11(c.__cpu);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_r11(c.__cpu, v);
            })
        .def_prop_rw(
            "r12",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_r12(c.__cpu);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_r12(c.__cpu, v);
            })
        .def_prop_rw(
            "r13",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_r13(c.__cpu);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_r13(c.__cpu, v);
            })
        .def_prop_rw(
            "r14",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_r14(c.__cpu);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_r14(c.__cpu, v);
            })
        .def_prop_rw(
            "r15",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_r15(c.__cpu);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_r15(c.__cpu, v);
            })
        .def_prop_rw(
            "rip",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_rip(c.__cpu);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_rip(c.__cpu, v);
            })
        .def_prop_rw(
            "rflags",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_rflags(c.__cpu);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_rflags(c.__cpu, v);
            })

        .def_prop_rw(
            "cs",
            [](BochsCPU::Cpu::CPU& c)
            {
                Seg s {};
                ::bochscpu_cpu_cs(c.__cpu, &s);
                return s;
            },
            [](BochsCPU::Cpu::CPU& c, Seg& s)
            {
                ::bochscpu_cpu_set_cs(c.__cpu, &s);
            })
        .def_prop_rw(
            "ds",
            [](BochsCPU::Cpu::CPU& c)
            {
                Seg s {};
                ::bochscpu_cpu_ds(c.__cpu, &s);
                return s;
            },
            [](BochsCPU::Cpu::CPU& c, Seg& s)
            {
                ::bochscpu_cpu_set_ds(c.__cpu, &s);
            })
        .def_prop_rw(
            "es",
            [](BochsCPU::Cpu::CPU& c)
            {
                Seg s {};
                ::bochscpu_cpu_es(c.__cpu, &s);
                return s;
            },
            [](BochsCPU::Cpu::CPU& c, Seg& s)
            {
                ::bochscpu_cpu_set_es(c.__cpu, &s);
            })
        .def_prop_rw(
            "fs",
            [](BochsCPU::Cpu::CPU& c)
            {
                Seg s {};
                ::bochscpu_cpu_fs(c.__cpu, &s);
                return s;
            },
            [](BochsCPU::Cpu::CPU& c, Seg& s)
            {
                ::bochscpu_cpu_set_fs(c.__cpu, &s);
            })
        .def_prop_rw(
            "ss",
            [](BochsCPU::Cpu::CPU& c)
            {
                Seg s {};
                ::bochscpu_cpu_ss(c.__cpu, &s);
                return s;
            },
            [](BochsCPU::Cpu::CPU& c, Seg& s)
            {
                ::bochscpu_cpu_set_ss(c.__cpu, &s);
            })
        .def_prop_rw(
            "gs",
            [](BochsCPU::Cpu::CPU& c)
            {
                Seg s {};
                ::bochscpu_cpu_gs(c.__cpu, &s);
                return s;
            },
            [](BochsCPU::Cpu::CPU& c, Seg& s)
            {
                ::bochscpu_cpu_set_gs(c.__cpu, &s);
            })
        .def_prop_rw(
            "ldtr",
            [](BochsCPU::Cpu::CPU& c)
            {
                Seg s {};
                ::bochscpu_cpu_ldtr(c.__cpu, &s);
                return s;
            },
            [](BochsCPU::Cpu::CPU& c, Seg& s)
            {
                ::bochscpu_cpu_set_ldtr(c.__cpu, &s);
            })
        .def_prop_rw(
            "tr",
            [](BochsCPU::Cpu::CPU& c)
            {
                Seg s {};
                ::bochscpu_cpu_tr(c.__cpu, &s);
                return s;
            },
            [](BochsCPU::Cpu::CPU& c, Seg& s)
            {
                ::bochscpu_cpu_set_tr(c.__cpu, &s);
            })
        .def_prop_rw(
            "gdtr",
            [](BochsCPU::Cpu::CPU& c)
            {
                GlobalSeg s {};
                ::bochscpu_cpu_gdtr(c.__cpu, &s);
                return s;
            },
            [](BochsCPU::Cpu::CPU& c, GlobalSeg& s)
            {
                ::bochscpu_cpu_set_gdtr(c.__cpu, &s);
            })
        .def_prop_rw(
            "idtr",
            [](BochsCPU::Cpu::CPU& c)
            {
                GlobalSeg s {};
                ::bochscpu_cpu_idtr(c.__cpu, &s);
                return s;
            },
            [](BochsCPU::Cpu::CPU& c, GlobalSeg& s)
            {
                ::bochscpu_cpu_set_idtr(c.__cpu, &s);
            })
        .def_prop_rw(
            "cr2",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_cr2(c.__cpu);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_cr2(c.__cpu, v);
            })
        .def_prop_rw(
            "cr3",
            [](BochsCPU::Cpu::CPU& c)
            {
                return ::bochscpu_cpu_cr3(c.__cpu);
            },
            [](BochsCPU::Cpu::CPU& c, uint64_t v)
            {
                ::bochscpu_cpu_set_cr3(c.__cpu, v);
            })
        .def_prop_rw(
            "zmm",
            [](BochsCPU::Cpu::CPU& c, uintptr_t idx)
            {
                Zmm z {};
                ::bochscpu_cpu_zmm(c.__cpu, idx, &z);
                return z;
            },
            [](BochsCPU::Cpu::CPU& c, uintptr_t idx, Zmm& z)
            {
                ::bochscpu_cpu_set_zmm(c.__cpu, idx, &z);
            });

#pragma endregion
}
