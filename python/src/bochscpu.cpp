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


int
bochscpu_tp_traverse(PyObject* self, visitproc visit, void* arg)
{
    BochsCPU::Session* sess = nb::inst_ptr<BochsCPU::Session>(self);
    nb::object value        = nb::find(sess->missing_page_handler);
    Py_VISIT(value.ptr());
    return 0;
}

int
bochscpu_tp_clear(PyObject* self)
{
    dbg("clearing PF handler");
    BochsCPU::Session* sess    = nb::inst_ptr<BochsCPU::Session>(self);
    sess->missing_page_handler = nullptr;
    return 0;
}

// Slot data structure referencing the above two functions
PyType_Slot slots[] = {
    {Py_tp_traverse, (void*)bochscpu_tp_traverse},
    {Py_tp_clear, (void*)bochscpu_tp_clear},
    {0, nullptr}};

NB_MODULE(bochscpu, m)
{
    //
    // Submodules
    //
    bochscpu_memory_module(m);
    bochscpu_cpu_module(m);

    //
    // Constants
    //
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

    nb::class_<BochsCPU::Hook>(m, "Hook")
        .def(nb::init<>())
        .def_rw("ctx", &BochsCPU::Hook::ctx)
        .def_rw("reset", &BochsCPU::Hook::reset)
        .def_rw("hlt", &BochsCPU::Hook::hlt)
        .def_rw("mwait", &BochsCPU::Hook::mwait)
        .def_rw("cnear_branch_taken", &BochsCPU::Hook::cnear_branch_taken)
        .def_rw("cnear_branch_not_taken", &BochsCPU::Hook::cnear_branch_not_taken)
        .def_rw("ucnear_branch", &BochsCPU::Hook::ucnear_branch)
        .def_rw("far_branch", &BochsCPU::Hook::far_branch)
        .def_rw("vmexit", &BochsCPU::Hook::vmexit)
        .def_rw("interrupt", &BochsCPU::Hook::interrupt)
        .def_rw("exception", &BochsCPU::Hook::exception)
        .def_rw("hw_interrupt", &BochsCPU::Hook::hw_interrupt)
        .def_rw("tlb_cntrl", &BochsCPU::Hook::tlb_cntrl)
        .def_rw("cache_cntrl", &BochsCPU::Hook::cache_cntrl)
        .def_rw("prefetch_hint", &BochsCPU::Hook::prefetch_hint)
        .def_rw("clflush", &BochsCPU::Hook::clflush)
        .def_rw("before_execution", &BochsCPU::Hook::before_execution)
        .def_rw("after_execution", &BochsCPU::Hook::after_execution)
        .def_rw("repeat_iteration", &BochsCPU::Hook::repeat_iteration)
        .def_rw("lin_access", &BochsCPU::Hook::lin_access)
        .def_rw("phy_access", &BochsCPU::Hook::phy_access)
        .def_rw("wrmsr", &BochsCPU::Hook::wrmsr)
        .def_rw("opcode", &BochsCPU::Hook::opcode)
        .def_rw("inp", &BochsCPU::Hook::inp)
        .def_rw("inp2", &BochsCPU::Hook::inp2)
        .def_rw("outp", &BochsCPU::Hook::outp);

    nb::class_<Seg>(m, "Segment")
        .def(nb::init<>())
        .def_rw("present", &Seg::present)
        .def_rw("selector", &Seg::selector)
        .def_rw("base", &Seg::base)
        .def_rw("limit", &Seg::limit)
        .def_rw("attr", &Seg::attr)
        .def(
            "__int__",
            [](Seg const& s)
            {
                return s.selector;
            });

    nb::class_<GlobalSeg>(m, "GlobalSegment")
        .def(nb::init<>())
        .def_rw("base", &GlobalSeg::base)
        .def_rw("limit", &GlobalSeg::limit);

    nb::class_<Zmm>(m, "Zmm").def(nb::init<>()).def_rw("q", &Zmm::q);

    nb::class_<State>(m, "State", nb::type_slots(slots))
        .def(nb::init<>())
        .def_rw("bochscpu_seed", &State::bochscpu_seed)
        .def_rw("rax", &State::rax)
        .def_rw("rcx", &State::rcx)
        .def_rw("rdx", &State::rdx)
        .def_rw("rbx", &State::rbx)
        .def_rw("rsp", &State::rsp)
        .def_rw("rbp", &State::rbp)
        .def_rw("rsi", &State::rsi)
        .def_rw("rdi", &State::rdi)
        .def_rw("r8", &State::r8)
        .def_rw("r9", &State::r9)
        .def_rw("r10", &State::r10)
        .def_rw("r11", &State::r11)
        .def_rw("r12", &State::r12)
        .def_rw("r13", &State::r13)
        .def_rw("r14", &State::r14)
        .def_rw("r15", &State::r15)
        .def_rw("rip", &State::rip)
        .def_rw("rflags", &State::rflags)
        .def_rw("es", &State::es)
        .def_rw("cs", &State::cs)
        .def_rw("ss", &State::ss)
        .def_rw("ds", &State::ds)
        .def_rw("fs", &State::fs)
        .def_rw("gs", &State::gs)
        .def_rw("ldtr", &State::ldtr)
        .def_rw("tr", &State::tr)
        .def_rw("gdtr", &State::gdtr)
        .def_rw("idtr", &State::idtr)
        .def_rw("cr0", &State::cr0)
        .def_rw("cr2", &State::cr2)
        .def_rw("cr3", &State::cr3)
        .def_rw("cr4", &State::cr4)
        .def_rw("cr8", &State::cr8)
        .def_rw("dr0", &State::dr0)
        .def_rw("dr1", &State::dr1)
        .def_rw("dr2", &State::dr2)
        .def_rw("dr3", &State::dr3)
        .def_rw("dr6", &State::dr6)
        .def_rw("dr7", &State::dr7)
        .def_rw("xcr0", &State::xcr0)
        .def_rw("zmm", &State::zmm)
        .def_rw("fpcw", &State::fpcw)
        .def_rw("fpsw", &State::fpsw)
        .def_rw("fptw", &State::fptw)
        .def_rw("fpop", &State::fpop)
        .def_rw("fpst", &State::fpst)
        .def_rw("mxcsr", &State::mxcsr)
        .def_rw("mxcsr_mask", &State::mxcsr_mask)
        .def_rw("tsc", &State::tsc)
        .def_rw("efer", &State::efer)
        .def_rw("kernel_gs_base", &State::kernel_gs_base)
        .def_rw("apic_base", &State::apic_base)
        .def_rw("pat", &State::pat)
        .def_rw("sysenter_cs", &State::sysenter_cs)
        .def_rw("sysenter_eip", &State::sysenter_eip)
        .def_rw("sysenter_esp", &State::sysenter_esp)
        .def_rw("star", &State::star)
        .def_rw("lstar", &State::lstar)
        .def_rw("cstar", &State::cstar)
        .def_rw("sfmask", &State::sfmask)
        .def_rw("tsc_aux", &State::tsc_aux);


    //
    // Exported native functions
    //
    {
        m.def(
            "bochscpu_mem_page_insert",
            [](uint64_t gpa, uintptr_t hva)
            {
                dbg("mapping GPA=%#llx <-> HVA=%#llx", gpa, hva);
                ::bochscpu_mem_page_insert(gpa, (uint8_t*)hva);
            },
            "Map a GPA to a HVA");
        m.def("bochscpu_mem_page_remove", &bochscpu_mem_page_remove, "gpa"_a);
        m.def(
            "bochscpu_mem_phy_translate",
            [](const uint64_t gpa)
            {
                return (uintptr_t)(::bochscpu_mem_phy_translate(gpa));
            },
            "gpa"_a);
        m.def("bochscpu_mem_virt_translate", &bochscpu_mem_virt_translate, "cr3"_a, "gva"_a);
        m.def(
            "bochscpu_mem_phy_read",
            [](uint64_t gpa, uintptr_t sz) -> std::vector<uint8_t>
            {
                std::vector<uint8_t> hva(sz);
                ::bochscpu_mem_phy_read(gpa, hva.data(), hva.size());
                return hva;
            },
            "gpa"_a,
            "size"_a,
            "Read from GPA");
        m.def(
            "bochscpu_mem_phy_write",
            [](uint64_t gpa, std::vector<uint8_t> const& hva)
            {
                ::bochscpu_mem_phy_write(gpa, hva.data(), hva.size());
            },
            "gpa"_a,
            "hva"_a,
            "Write to GPA");
        m.def(
            "bochscpu_mem_virt_write",
            [](uint64_t cr3, uint64_t gva, std::vector<uint8_t> const& hva)
            {
                return ::bochscpu_mem_virt_write(cr3, gva, hva.data(), hva.size()) == 0;
            },
            "cr3"_a,
            "gva"_a,
            "hva"_a,
            "Write to GVA");
        m.def(
            "bochscpu_mem_virt_read",
            [](uint64_t cr3, uint64_t gva, const uint64_t sz) -> std::vector<uint8_t>
            {
                std::vector<uint8_t> hva(sz);
                if ( ::bochscpu_mem_virt_read(cr3, gva, hva.data(), hva.size()) )
                    throw std::runtime_error("invalid access");
                return hva;
            },
            "cr3"_a,
            "gva"_a,
            "sz"_a,
            "Read from GVA");
        m.def("bochscpu_log_set_level", &bochscpu_log_set_level, "level"_a);
        m.def("instr_bx_opcode", &bochscpu_instr_bx_opcode, "p"_a);
        m.def("instr_imm16", &bochscpu_instr_imm16, "p"_a);
        m.def("instr_imm32", &bochscpu_instr_imm32, "p"_a);
        m.def("instr_imm64", &bochscpu_instr_imm64, "p"_a);


        nb::class_<BochsCPU::Session>(m, "session", nb::type_slots(slots))
            .def(nb::init<>())
            .def_rw("missing_page_handler", &BochsCPU::Session::missing_page_handler, "Set the missing page callback")
            .def_ro("cpu", &BochsCPU::Session::cpu, "Get the CPU associated to the session")
            .def(
                "run",
                [](BochsCPU::Session& s, std::vector<BochsCPU::Hook>& h)
                {
                    if ( h.size() > (MAX_HOOKS - 1) )
                        throw std::runtime_error("Too many hooks");

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
}
