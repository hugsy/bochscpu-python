#include "bochscpu.hpp"

#include <nanobind/nanobind.h>
#include <nanobind/stl/array.h>
#include <nanobind/stl/function.h>
#include <nanobind/stl/list.h>
#include <nanobind/stl/vector.h>


namespace nb = nanobind;
using namespace nb::literals;

#define MAX_HOOKS 256


void
bochscpu_memory_module(nb::module_& m);

void
bochscpu_cpu_module(nb::module_& m);


static int
bochscpu_tp_traverse(PyObject* self, visitproc visit, void* arg)
{
    BochsCPU::Session* sess = nb::inst_ptr<BochsCPU::Session>(self);
    nb::object value        = nb::find(sess->missing_page_handler);
    Py_VISIT(value.ptr());
    return 0;
}

static int
bochscpu_tp_clear(PyObject* self)
{
    dbg("clearing PF handler");
    BochsCPU::Session* sess    = nb::inst_ptr<BochsCPU::Session>(self);
    sess->missing_page_handler = nullptr;
    return 0;
}

PyType_Slot slots[] = {
    {Py_tp_traverse, (void*)bochscpu_tp_traverse},
    {Py_tp_clear, (void*)bochscpu_tp_clear},
    {0, nullptr}};

NB_MODULE(bochscpu, m)
{
    m.doc() = "The `bochscpu` module";

    //
    // Submodules
    //
    bochscpu_memory_module(m);
    bochscpu_cpu_module(m);

    nb::enum_<BochsCPU::InstructionType>(m, "InstructionType", "Class InstructionType")
        .value("IS_JMP", BochsCPU::InstructionType::BX_INSTR_IS_JMP, "Constant value for BX_INSTR_IS_JMP")
        .value(
            "IS_JMP_INDIRECT",
            BochsCPU::InstructionType::BOCHSCPU_INSTR_IS_JMP_INDIRECT,
            "Constant value for BOCHSCPU_INSTR_IS_JMP_INDIRECT")
        .value(
            "IS_CALL",
            BochsCPU::InstructionType::BOCHSCPU_INSTR_IS_CALL,
            "Constant value for BOCHSCPU_INSTR_IS_CALL")
        .value(
            "IS_CALL_INDIRECT",
            BochsCPU::InstructionType::BOCHSCPU_INSTR_IS_CALL_INDIRECT,
            "Constant value for BOCHSCPU_INSTR_IS_CALL_INDIRECT")
        .value("IS_RET", BochsCPU::InstructionType::BOCHSCPU_INSTR_IS_RET, "Constant value for BOCHSCPU_INSTR_IS_RET")
        .value(
            "IS_IRET",
            BochsCPU::InstructionType::BOCHSCPU_INSTR_IS_IRET,
            "Constant value for BOCHSCPU_INSTR_IS_IRET")
        .value("IS_INT", BochsCPU::InstructionType::BOCHSCPU_INSTR_IS_INT, "Constant value for BOCHSCPU_INSTR_IS_INT")
        .value(
            "IS_SYSCALL",
            BochsCPU::InstructionType::BOCHSCPU_INSTR_IS_SYSCALL,
            "Constant value for BOCHSCPU_INSTR_IS_SYSCALL")
        .value(
            "IS_SYSRET",
            BochsCPU::InstructionType::BOCHSCPU_INSTR_IS_SYSRET,
            "Constant value for BOCHSCPU_INSTR_IS_SYSRET")
        .value(
            "IS_SYSENTER",
            BochsCPU::InstructionType::BOCHSCPU_INSTR_IS_SYSENTER,
            "Constant value for BOCHSCPU_INSTR_IS_SYSENTER")
        .value(
            "IS_SYSEXIT",
            BochsCPU::InstructionType::BOCHSCPU_INSTR_IS_SYSEXIT,
            "Constant value for BOCHSCPU_INSTR_IS_SYSEXIT")
        .export_values();


    nb::enum_<BochsCPU::HookType>(m, "HookType", "Class HookType")
        .value("MEM_READ", BochsCPU::HookType::BOCHSCPU_HOOK_MEM_READ, "Constant value for BOCHSCPU_HOOK_MEM_READ")
        .value("MEM_WRITE", BochsCPU::HookType::BOCHSCPU_HOOK_MEM_WRITE, "Constant value for BOCHSCPU_HOOK_MEM_WRITE")
        .value(
            "MEM_EXECUTE",
            BochsCPU::HookType::BOCHSCPU_HOOK_MEM_EXECUTE,
            "Constant value for BOCHSCPU_HOOK_MEM_EXECUTE")
        .value("MEM_RW", BochsCPU::HookType::BOCHSCPU_HOOK_MEM_RW, "Constant value for BOCHSCPU_HOOK_MEM_RW")
        .value("TLB_CR0", BochsCPU::HookType::BOCHSCPU_HOOK_TLB_CR0, "Constant value for BOCHSCPU_HOOK_TLB_CR0")
        .value("TLB_CR3", BochsCPU::HookType::BOCHSCPU_HOOK_TLB_CR3, "Constant value for BOCHSCPU_HOOK_TLB_CR3")
        .value("TLB_CR4", BochsCPU::HookType::BOCHSCPU_HOOK_TLB_CR4, "Constant value for BOCHSCPU_HOOK_TLB_CR4")
        .value(
            "TLB_TASKSWITCH",
            BochsCPU::HookType::BOCHSCPU_HOOK_TLB_TASKSWITCH,
            "Constant value for BOCHSCPU_HOOK_TLB_TASKSWITCH")
        .value(
            "TLB_CONTEXTSWITCH",
            BochsCPU::HookType::BOCHSCPU_HOOK_TLB_CONTEXTSWITCH,
            "Constant value for BOCHSCPU_HOOK_TLB_CONTEXTSWITCH")
        .value(
            "TLB_INVLPG",
            BochsCPU::HookType::BOCHSCPU_HOOK_TLB_INVLPG,
            "Constant value for BOCHSCPU_HOOK_TLB_INVLPG")
        .value(
            "TLB_INVEPT",
            BochsCPU::HookType::BOCHSCPU_HOOK_TLB_INVEPT,
            "Constant value for BOCHSCPU_HOOK_TLB_INVEPT")
        .value(
            "TLB_INVVPID",
            BochsCPU::HookType::BOCHSCPU_HOOK_TLB_INVVPID,
            "Constant value for BOCHSCPU_HOOK_TLB_INVVPID")
        .value(
            "TLB_INVPCID",
            BochsCPU::HookType::BOCHSCPU_HOOK_TLB_INVPCID,
            "Constant value for BOCHSCPU_HOOK_TLB_INVPCID")
        .export_values();


    nb::enum_<BochsCPU::OpcodeOperationType>(m, "OpcodeOperationType", "Class OpcodeOperationType")
        .value(
            "OPERATION_ERROR",
            BochsCPU::OpcodeOperationType::BOCHSCPU_OPCODE_ERROR,
            "Constant value for BOCHSCPU_OPCODE_ERROR")
        .value(
            "OPERATION_INSERTED",
            BochsCPU::OpcodeOperationType::BOCHSCPU_OPCODE_INSERTED,
            "Constant value for BOCHSCPU_OPCODE_INSERTED")
        .export_values();


    nb::class_<BochsCPU::Hook>(m, "Hook", "Class Hook")
        .def(nb::init<>())
        .def_rw("ctx", &BochsCPU::Hook::ctx, "A raw pointer to the Session object")
        .def_rw("reset", &BochsCPU::Hook::reset, "Callback for Bochs `reset` callback")
        .def_rw("hlt", &BochsCPU::Hook::hlt, "Callback for Bochs `hlt` callback")
        .def_rw("mwait", &BochsCPU::Hook::mwait, "Callback for Bochs `mwait` callback")
        .def_rw(
            "cnear_branch_taken",
            &BochsCPU::Hook::cnear_branch_taken,
            "Callback for Bochs `cnear_branch_taken` callback")
        .def_rw(
            "cnear_branch_not_taken",
            &BochsCPU::Hook::cnear_branch_not_taken,
            "Callback for Bochs `cnear_branch_not_taken` callback")
        .def_rw("ucnear_branch", &BochsCPU::Hook::ucnear_branch, "Callback for Bochs `ucnear_branch` callback")
        .def_rw("far_branch", &BochsCPU::Hook::far_branch, "Callback for Bochs `far_branch` callback")
        .def_rw("vmexit", &BochsCPU::Hook::vmexit, "Callback for Bochs `vmexit` callback")
        .def_rw("interrupt", &BochsCPU::Hook::interrupt, "Callback for Bochs `interrupt` callback")
        .def_rw("exception", &BochsCPU::Hook::exception, "Callback for Bochs `exception` callback")
        .def_rw("hw_interrupt", &BochsCPU::Hook::hw_interrupt, "Callback for Bochs `hw_interrupt` callback")
        .def_rw("tlb_cntrl", &BochsCPU::Hook::tlb_cntrl, "Callback for Bochs `tlb_cntrl` callback")
        .def_rw("cache_cntrl", &BochsCPU::Hook::cache_cntrl, "Callback for Bochs `cache_cntrl` callback")
        .def_rw("prefetch_hint", &BochsCPU::Hook::prefetch_hint, "Callback for Bochs `prefetch_hint` callback")
        .def_rw("clflush", &BochsCPU::Hook::clflush, "Callback for Bochs `clflush` callback")
        .def_rw("before_execution", &BochsCPU::Hook::before_execution, "Callback for Bochs `before_execution` callback")
        .def_rw("after_execution", &BochsCPU::Hook::after_execution, "Callback for Bochs `after_execution` callback")
        .def_rw("repeat_iteration", &BochsCPU::Hook::repeat_iteration, "Callback for Bochs `repeat_iteration` callback")
        .def_rw("lin_access", &BochsCPU::Hook::lin_access, "Callback for Bochs `lin_access` callback")
        .def_rw("phy_access", &BochsCPU::Hook::phy_access, "Callback for Bochs `phy_access` callback")
        .def_rw("wrmsr", &BochsCPU::Hook::wrmsr, "Callback for Bochs `wrmsr` callback")
        .def_rw("opcode", &BochsCPU::Hook::opcode, "Callback for Bochs `opcode` callback")
        .def_rw("inp", &BochsCPU::Hook::inp, "Callback for Bochs `inp` callback")
        .def_rw("inp2", &BochsCPU::Hook::inp2, "Callback for Bochs `inp2` callback")
        .def_rw("outp", &BochsCPU::Hook::outp, "Callback for Bochs `outp` callback");

    nb::class_<Seg>(m, "Segment", "Segment class")
        .def(nb::init<>())
        .def_rw("present", &Seg::present, "Get/Set the Segment `present` attribute")
        .def_rw("selector", &Seg::selector, "Get/Set the Segment `selector` attribute")
        .def_rw("base", &Seg::base, "Get/Set the Segment `base` attribute")
        .def_rw("limit", &Seg::limit, "Get/Set the Segment `limit` attribute")
        .def_rw("attr", &Seg::attr, "Get/Set the Segment `attr` attribute")
        .def(
            "__int__",
            [](Seg const& s)
            {
                return s.selector;
            });

    nb::class_<GlobalSeg>(m, "GlobalSegment", "GlobalSegment class")
        .def(nb::init<>())
        .def_rw("base", &GlobalSeg::base, "Get/Set the GlobalSegment `base` attribute")
        .def_rw("limit", &GlobalSeg::limit, "Get/Set the GlobalSegment `limit` attribute");

    nb::class_<Zmm>(m, "Zmm").def(nb::init<>()).def_rw("q", &Zmm::q);

    nb::class_<State>(m, "State", nb::type_slots(slots), "Class State")
        .def(nb::init<>())
        .def_rw("seed", &State::bochscpu_seed, "Get/Set the seed in the current state")
        .def_rw("rax", &State::rax, "Get/Set the register `rax` in the current state")
        .def_rw("rcx", &State::rcx, "Get/Set the register `rcx` in the current state")
        .def_rw("rdx", &State::rdx, "Get/Set the register `rdx` in the current state")
        .def_rw("rbx", &State::rbx, "Get/Set the register `rbx` in the current state")
        .def_rw("rsp", &State::rsp, "Get/Set the register `rsp` in the current state")
        .def_rw("rbp", &State::rbp, "Get/Set the register `rbp` in the current state")
        .def_rw("rsi", &State::rsi, "Get/Set the register `rsi` in the current state")
        .def_rw("rdi", &State::rdi, "Get/Set the register `rdi` in the current state")
        .def_rw("r8", &State::r8, "Get/Set the register `r8` in the current state")
        .def_rw("r9", &State::r9, "Get/Set the register `r9` in the current state")
        .def_rw("r10", &State::r10, "Get/Set the register `r10` in the current state")
        .def_rw("r11", &State::r11, "Get/Set the register `r11` in the current state")
        .def_rw("r12", &State::r12, "Get/Set the register `r12` in the current state")
        .def_rw("r13", &State::r13, "Get/Set the register `r13` in the current state")
        .def_rw("r14", &State::r14, "Get/Set the register `r14` in the current state")
        .def_rw("r15", &State::r15, "Get/Set the register `r15` in the current state")
        .def_rw("rip", &State::rip, "Get/Set the register `rip` in the current state")
        .def_rw("rflags", &State::rflags, "Get/Set the register `rflags` in the current state")
        .def_rw("es", &State::es, "Get/Set the register `es` in the current state")
        .def_rw("cs", &State::cs, "Get/Set the register `cs` in the current state")
        .def_rw("ss", &State::ss, "Get/Set the register `ss` in the current state")
        .def_rw("ds", &State::ds, "Get/Set the register `ds` in the current state")
        .def_rw("fs", &State::fs, "Get/Set the register `fs` in the current state")
        .def_rw("gs", &State::gs, "Get/Set the register `gs` in the current state")
        .def_rw("ldtr", &State::ldtr, "Get/Set the register `ldtr` in the current state")
        .def_rw("tr", &State::tr, "Get/Set the register `tr` in the current state")
        .def_rw("gdtr", &State::gdtr, "Get/Set the register `gdtr` in the current state")
        .def_rw("idtr", &State::idtr, "Get/Set the register `idtr` in the current state")
        .def_rw("cr0", &State::cr0, "Get/Set the register `cr0` in the current state")
        .def_rw("cr2", &State::cr2, "Get/Set the register `cr2` in the current state")
        .def_rw("cr3", &State::cr3, "Get/Set the register `cr3` in the current state")
        .def_rw("cr4", &State::cr4, "Get/Set the register `cr4` in the current state")
        .def_rw("cr8", &State::cr8, "Get/Set the register `cr8` in the current state")
        .def_rw("dr0", &State::dr0, "Get/Set the register `dr0` in the current state")
        .def_rw("dr1", &State::dr1, "Get/Set the register `dr1` in the current state")
        .def_rw("dr2", &State::dr2, "Get/Set the register `dr2` in the current state")
        .def_rw("dr3", &State::dr3, "Get/Set the register `dr3` in the current state")
        .def_rw("dr6", &State::dr6, "Get/Set the register `dr6` in the current state")
        .def_rw("dr7", &State::dr7, "Get/Set the register `dr7` in the current state")
        .def_rw("xcr0", &State::xcr0, "Get/Set the register `xcr0` in the current state")
        .def_rw("zmm", &State::zmm, "Get/Set the register `zmm` in the current state")
        .def_rw("fpcw", &State::fpcw, "Get/Set the register `fpcw` in the current state")
        .def_rw("fpsw", &State::fpsw, "Get/Set the register `fpsw` in the current state")
        .def_rw("fptw", &State::fptw, "Get/Set the register `fptw` in the current state")
        .def_rw("fpop", &State::fpop, "Get/Set the register `fpop` in the current state")
        .def_rw("fpst", &State::fpst, "Get/Set the register `fpst` in the current state")
        .def_rw("mxcsr", &State::mxcsr, "Get/Set the register `mxcsr` in the current state")
        .def_rw("mxcsr_mask", &State::mxcsr_mask, "Get/Set the register `mxcsr_mask` in the current state")
        .def_rw("tsc", &State::tsc, "Get/Set the register `tsc` in the current state")
        .def_rw("efer", &State::efer, "Get/Set the register `efer` in the current state")
        .def_rw("kernel_gs_base", &State::kernel_gs_base, "Get/Set the register `kernel_gs_base` in the current state")
        .def_rw("apic_base", &State::apic_base, "Get/Set the register `apic_base` in the current state")
        .def_rw("pat", &State::pat, "Get/Set the register `pat` in the current state")
        .def_rw("sysenter_cs", &State::sysenter_cs, "Get/Set the register `sysenter_cs` in the current state")
        .def_rw("sysenter_eip", &State::sysenter_eip, "Get/Set the register `sysenter_eip` in the current state")
        .def_rw("sysenter_esp", &State::sysenter_esp, "Get/Set the register `sysenter_esp` in the current state")
        .def_rw("star", &State::star, "Get/Set the register `star` in the current state")
        .def_rw("lstar", &State::lstar, "Get/Set the register `lstar` in the current state")
        .def_rw("cstar", &State::cstar, "Get/Set the register `cstar` in the current state")
        .def_rw("sfmask", &State::sfmask, "Get/Set the register `sfmask` in the current state")
        .def_rw("tsc_aux", &State::tsc_aux, "Get/Set the register `tsc_aux` in the current state");


    //
    // Exported native constants & functions
    //
    {
        m.attr("BX_INSTR_IS_JMP")                 = BX_INSTR_IS_JMP;
        m.attr("BOCHSCPU_INSTR_IS_JMP_INDIRECT")  = BOCHSCPU_INSTR_IS_JMP_INDIRECT;
        m.attr("BOCHSCPU_INSTR_IS_CALL")          = BOCHSCPU_INSTR_IS_CALL;
        m.attr("BOCHSCPU_INSTR_IS_CALL_INDIRECT") = BOCHSCPU_INSTR_IS_CALL_INDIRECT;
        m.attr("BOCHSCPU_INSTR_IS_RET")           = BOCHSCPU_INSTR_IS_RET;
        m.attr("BOCHSCPU_INSTR_IS_IRET")          = BOCHSCPU_INSTR_IS_IRET;
        m.attr("BOCHSCPU_INSTR_IS_INT")           = BOCHSCPU_INSTR_IS_INT;
        m.attr("BOCHSCPU_INSTR_IS_SYSCALL")       = BOCHSCPU_INSTR_IS_SYSCALL;
        m.attr("BOCHSCPU_INSTR_IS_SYSRET")        = BOCHSCPU_INSTR_IS_SYSRET;
        m.attr("BOCHSCPU_INSTR_IS_SYSENTER")      = BOCHSCPU_INSTR_IS_SYSENTER;
        m.attr("BOCHSCPU_INSTR_IS_SYSEXIT")       = BOCHSCPU_INSTR_IS_SYSEXIT;
        m.attr("BOCHSCPU_HOOK_MEM_READ")          = BOCHSCPU_HOOK_MEM_READ;
        m.attr("BOCHSCPU_HOOK_MEM_WRITE")         = BOCHSCPU_HOOK_MEM_WRITE;
        m.attr("BOCHSCPU_HOOK_MEM_EXECUTE")       = BOCHSCPU_HOOK_MEM_EXECUTE;
        m.attr("BOCHSCPU_HOOK_MEM_RW")            = BOCHSCPU_HOOK_MEM_RW;
        m.attr("BOCHSCPU_HOOK_TLB_CR0")           = BOCHSCPU_HOOK_TLB_CR0;
        m.attr("BOCHSCPU_HOOK_TLB_CR3")           = BOCHSCPU_HOOK_TLB_CR3;
        m.attr("BOCHSCPU_HOOK_TLB_CR4")           = BOCHSCPU_HOOK_TLB_CR4;
        m.attr("BOCHSCPU_HOOK_TLB_TASKSWITCH")    = BOCHSCPU_HOOK_TLB_TASKSWITCH;
        m.attr("BOCHSCPU_HOOK_TLB_CONTEXTSWITCH") = BOCHSCPU_HOOK_TLB_CONTEXTSWITCH;
        m.attr("BOCHSCPU_HOOK_TLB_INVLPG")        = BOCHSCPU_HOOK_TLB_INVLPG;
        m.attr("BOCHSCPU_HOOK_TLB_INVEPT")        = BOCHSCPU_HOOK_TLB_INVEPT;
        m.attr("BOCHSCPU_HOOK_TLB_INVVPID")       = BOCHSCPU_HOOK_TLB_INVVPID;
        m.attr("BOCHSCPU_HOOK_TLB_INVPCID")       = BOCHSCPU_HOOK_TLB_INVPCID;
        m.attr("BOCHSCPU_OPCODE_ERROR")           = BOCHSCPU_OPCODE_ERROR;
        m.attr("BOCHSCPU_OPCODE_INSERTED")        = BOCHSCPU_OPCODE_INSERTED;

        m.def("bochscpu_log_set_level", &bochscpu_log_set_level, "level"_a, "Set verbosity level");
        m.def("instr_bx_opcode", &bochscpu_instr_bx_opcode, "p"_a);
        m.def("instr_imm16", &bochscpu_instr_imm16, "p"_a);
        m.def("instr_imm32", &bochscpu_instr_imm32, "p"_a);
        m.def("instr_imm64", &bochscpu_instr_imm64, "p"_a);
    }

    nb::class_<BochsCPU::Session>(m, "session", nb::type_slots(slots), "Class session")
        .def(nb::init<>())
        .def_rw("missing_page_handler", &BochsCPU::Session::missing_page_handler, "Set the missing page callback")
        .def_ro("cpu", &BochsCPU::Session::cpu, "Get the CPU associated to the session")
        .def(
            "run",
            [](BochsCPU::Session& s, std::vector<BochsCPU::Hook>& h)
            {
                if ( h.size() > (MAX_HOOKS - 1) )
                {
                    throw std::runtime_error("Too many hooks.");
                }

                bochscpu_hooks_t hooks[MAX_HOOKS] {};
                bochscpu_hooks_t* hooks2[MAX_HOOKS] {};

                for ( int i = 0; BochsCPU::Hook & _h : h )
                {
                    _h.ctx                          = (void*)&s;
                    hooks[i].ctx                    = (void*)&_h;
                    hooks[i].before_execution       = BochsCPU::Callbacks::before_execution_cb;
                    hooks[i].after_execution        = BochsCPU::Callbacks::after_execution_cb;
                    hooks[i].reset                  = BochsCPU::Callbacks::reset_cb;
                    hooks[i].hlt                    = BochsCPU::Callbacks::hlt_cb;
                    hooks[i].mwait                  = BochsCPU::Callbacks::mwait_cb;
                    hooks[i].cnear_branch_taken     = BochsCPU::Callbacks::cnear_branch_taken_cb;
                    hooks[i].cnear_branch_not_taken = BochsCPU::Callbacks::cnear_branch_not_taken_cb;
                    hooks[i].ucnear_branch          = BochsCPU::Callbacks::ucnear_branch_cb;
                    hooks[i].far_branch             = BochsCPU::Callbacks::far_branch_cb;
                    hooks[i].vmexit                 = BochsCPU::Callbacks::vmexit_cb;
                    hooks[i].interrupt              = BochsCPU::Callbacks::interrupt_cb;
                    hooks[i].hw_interrupt           = BochsCPU::Callbacks::hw_interrupt_cb;
                    hooks[i].clflush                = BochsCPU::Callbacks::clflush_cb;
                    hooks[i].tlb_cntrl              = BochsCPU::Callbacks::tlb_cntrl_cb;
                    hooks[i].cache_cntrl            = BochsCPU::Callbacks::cache_cntrl_cb;
                    hooks[i].prefetch_hint          = BochsCPU::Callbacks::prefetch_hint_cb;
                    hooks[i].wrmsr                  = BochsCPU::Callbacks::wrmsr_cb;
                    hooks[i].repeat_iteration       = BochsCPU::Callbacks::repeat_iteration_cb;
                    hooks[i].lin_access             = BochsCPU::Callbacks::lin_access_cb;
                    hooks[i].phy_access             = BochsCPU::Callbacks::phy_access_cb;
                    hooks[i].inp                    = BochsCPU::Callbacks::inp_cb;
                    hooks[i].inp2                   = BochsCPU::Callbacks::inp2_cb;
                    hooks[i].outp                   = BochsCPU::Callbacks::outp_cb;
                    hooks[i].opcode                 = BochsCPU::Callbacks::opcode_cb;
                    hooks[i].exception              = BochsCPU::Callbacks::exception_cb;
                    hooks2[i]                       = &hooks[i];
                    i++;
                }

                ::bochscpu_cpu_run(&s.cpu, hooks2);
            },
            "Start the execution with a set of hooks")
        .def(
            "stop",
            [](BochsCPU::Session& s)
            {
                ::bochscpu_cpu_stop(&s.cpu);
            },
            "Stop the execution");
}
