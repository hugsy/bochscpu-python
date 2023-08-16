#include "bochscpu.hpp"

#define EXECUTE_CB(c, n, ...)                                                                                          \
    {                                                                                                                  \
        Hook* ptr = (Hook*)ctx;                                                                                        \
        if ( !ptr )                                                                                                    \
            throw std::runtime_error("");                                                                              \
        if ( !ptr->n )                                                                                                 \
            return;                                                                                                    \
        ptr->n(ptr->ctx, __VA_ARGS__);                                                                                 \
    }

namespace BochsCPU::Callbacks
{


void
before_execution_cb(context_t* ctx, uint32_t cpu_id, void* insn)
{
    EXECUTE_CB(ctx, before_execution, cpu_id, insn);
}


void
after_execution_cb(context_t* ctx, uint32_t cpu_id, void* insn)
{
    EXECUTE_CB(ctx, after_execution, cpu_id, insn);
}

void
reset_cb(context_t* ctx, uint32_t cpu_id, unsigned int type)
{
    EXECUTE_CB(ctx, reset, cpu_id, type);
}

void
hlt_cb(context_t* ctx, uint32_t cpu_id)
{
    EXECUTE_CB(ctx, hlt, cpu_id);
}

void
mwait_cb(context_t* ctx, uint32_t cpu_id, uint64_t addr, uintptr_t len, uint32_t flags)
{
    EXECUTE_CB(ctx, mwait, cpu_id, addr, len, flags);
}

void
cnear_branch_taken_cb(context_t* ctx, uint32_t cpu_id, uint64_t branch_eip, uint64_t new_branch_eip)
{
    EXECUTE_CB(ctx, cnear_branch_taken, cpu_id, branch_eip, new_branch_eip);
}

void
cnear_branch_not_taken_cb(context_t* ctx, uint32_t cpu_id, uint64_t branch_eip, uint64_t new_branch_eip)
{
    EXECUTE_CB(ctx, cnear_branch_not_taken, cpu_id, branch_eip, new_branch_eip);
}

void
ucnear_branch_cb(context_t* ctx, uint32_t cpu_id, unsigned what, uint64_t branch_eip, uint64_t new_eip)
{
    EXECUTE_CB(ctx, ucnear_branch, cpu_id, what, branch_eip, new_eip);
}

void
far_branch_cb(
    context_t* ctx,
    uint32_t cpu_id,
    uint32_t what,
    uint16_t new_cs,
    uint64_t new_eip,
    uint16_t cs,
    uint64_t eip)
{
    EXECUTE_CB(ctx, far_branch, cpu_id, what, new_cs, new_eip, cs, eip);
}

void
vmexit_cb(context_t* ctx, uint32_t cpu_id, uint32_t reason, uint64_t qualification)

{
    EXECUTE_CB(ctx, vmexit, cpu_id, reason, qualification);
}

void
interrupt_cb(context_t* ctx, uint32_t cpu_id, unsigned vector)
{
    EXECUTE_CB(ctx, interrupt, cpu_id, vector);
}

void
hw_interrupt_cb(context_t* ctx, uint32_t cpu_id, unsigned vector, uint16_t cs, uint64_t eip)
{
    EXECUTE_CB(ctx, hw_interrupt, cpu_id, vector, cs, eip);
}

void
clflush_cb(context_t* ctx, uint32_t cpu_id, uint64_t laddr, uint64_t paddr)
{
    EXECUTE_CB(ctx, clflush, cpu_id, laddr, paddr);
}

void
tlb_cntrl_cb(context_t* ctx, uint32_t cpu_id, unsigned what, uint64_t new_cr_value)
{
    EXECUTE_CB(ctx, tlb_cntrl, cpu_id, what, new_cr_value);
}

void
cache_cntrl_cb(context_t* ctx, uint32_t cpu_id, unsigned what)
{
    EXECUTE_CB(ctx, cache_cntrl, cpu_id, what);
}

void
prefetch_hint_cb(context_t* ctx, uint32_t cpu_id, unsigned what, unsigned seg, uint64_t offset)
{
    EXECUTE_CB(ctx, prefetch_hint, cpu_id, what, seg, offset);
}

void
wrmsr_cb(context_t* ctx, uint32_t cpu_id, unsigned msr, uint64_t value)
{
    EXECUTE_CB(ctx, wrmsr, cpu_id, msr, value);
}

void
repeat_iteration_cb(context_t* ctx, uint32_t cpu_id, void* insn)
{
    EXECUTE_CB(ctx, repeat_iteration, cpu_id, insn);
}

void
lin_access_cb(context_t* ctx, uint32_t cpu_id, uint64_t lin, uint64_t phy, uintptr_t len, uint32_t rw, uint32_t access)
{
    EXECUTE_CB(ctx, lin_access, cpu_id, lin, phy, len, rw, access);
}

void
phy_access_cb(context_t* ctx, uint32_t cpu_id, uint64_t lin, uintptr_t phy, uint32_t len, uint32_t rw)
{
    EXECUTE_CB(ctx, phy_access, cpu_id, lin, phy, len, rw);
}

void
inp_cb(context_t* ctx, uint16_t cpu_id, uintptr_t len)
{
    EXECUTE_CB(ctx, inp, cpu_id, len);
}

void
inp2_cb(context_t* ctx, uint16_t cpu_id, uintptr_t len, unsigned val)
{
    EXECUTE_CB(ctx, inp2, cpu_id, len, val);
}

void
outp_cb(context_t* ctx, uint16_t cpu_id, uintptr_t len, unsigned val)
{
    EXECUTE_CB(ctx, outp, cpu_id, len, val);
}

void
opcode_cb(context_t* ctx, uint32_t cpu_id, void* insn, uint8_t* opcode, uintptr_t len, bool is32, bool is64)
{
    EXECUTE_CB(ctx, opcode, cpu_id, insn, opcode, len, is32, is64);
}

void
exception_cb(context_t* ctx, uint32_t cpu_id, unsigned vector, unsigned error_code)
{
    EXECUTE_CB(ctx, exception, cpu_id, vector, error_code);
}


}; // namespace BochsCPU::Callbacks