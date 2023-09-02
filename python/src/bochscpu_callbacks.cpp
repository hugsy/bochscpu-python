#include "bochscpu.hpp"

#define ExecuteCallback(Context, Name, ...)                                                                            \
    {                                                                                                                  \
        if ( !Context )                                                                                                \
        {                                                                                                              \
            err("Context for callback '" #Name "' is unexpectedly null");                                              \
            return;                                                                                                    \
        }                                                                                                              \
        BochsCPU::Hook* hook    = reinterpret_cast<BochsCPU::Hook*>(Context);                                          \
        BochsCPU::Session* sess = (BochsCPU::Session*)hook->ctx;                                                       \
        if ( !sess )                                                                                                   \
        {                                                                                                              \
            err("Session for BochsCPU::Hook(%p)->" #Name " is null", hook);                                            \
            return;                                                                                                    \
        }                                                                                                              \
        if ( hook->Name )                                                                                              \
        {                                                                                                              \
            hook->Name(sess, __VA_ARGS__);                                                                             \
            return;                                                                                                    \
        }                                                                                                              \
        dbg("Callback BochsCPU::Hook(%p)->" #Name " in Session(%p) is null", sess, hook);                              \
        return;                                                                                                        \
    }

namespace BochsCPU::Callbacks
{


void
before_execution_cb(context_t* ctx, uint32_t cpu_id, void* insn)
{
    ExecuteCallback(ctx, before_execution, cpu_id, insn);
}


void
after_execution_cb(context_t* ctx, uint32_t cpu_id, void* insn)
{
    ExecuteCallback(ctx, after_execution, cpu_id, insn);
}

void
reset_cb(context_t* ctx, uint32_t cpu_id, unsigned int type)
{
    ExecuteCallback(ctx, reset, cpu_id, type);
}

void
hlt_cb(context_t* ctx, uint32_t cpu_id)
{
    ExecuteCallback(ctx, hlt, cpu_id);
}

void
mwait_cb(context_t* ctx, uint32_t cpu_id, uint64_t addr, uintptr_t len, uint32_t flags)
{
    ExecuteCallback(ctx, mwait, cpu_id, addr, len, flags);
}

void
cnear_branch_taken_cb(context_t* ctx, uint32_t cpu_id, uint64_t branch_eip, uint64_t new_branch_eip)
{
    ExecuteCallback(ctx, cnear_branch_taken, cpu_id, branch_eip, new_branch_eip);
}

void
cnear_branch_not_taken_cb(context_t* ctx, uint32_t cpu_id, uint64_t branch_eip, uint64_t new_branch_eip)
{
    ExecuteCallback(ctx, cnear_branch_not_taken, cpu_id, branch_eip, new_branch_eip);
}

void
ucnear_branch_cb(context_t* ctx, uint32_t cpu_id, unsigned what, uint64_t branch_eip, uint64_t new_eip)
{
    ExecuteCallback(ctx, ucnear_branch, cpu_id, what, branch_eip, new_eip);
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
    ExecuteCallback(ctx, far_branch, cpu_id, what, new_cs, new_eip, cs, eip);
}

void
vmexit_cb(context_t* ctx, uint32_t cpu_id, uint32_t reason, uint64_t qualification)

{
    ExecuteCallback(ctx, vmexit, cpu_id, reason, qualification);
}

void
interrupt_cb(context_t* ctx, uint32_t cpu_id, unsigned vector)
{
    ExecuteCallback(ctx, interrupt, cpu_id, vector);
}

void
hw_interrupt_cb(context_t* ctx, uint32_t cpu_id, unsigned vector, uint16_t cs, uint64_t eip)
{
    ExecuteCallback(ctx, hw_interrupt, cpu_id, vector, cs, eip);
}

void
clflush_cb(context_t* ctx, uint32_t cpu_id, uint64_t laddr, uint64_t paddr)
{
    ExecuteCallback(ctx, clflush, cpu_id, laddr, paddr);
}

void
tlb_cntrl_cb(context_t* ctx, uint32_t cpu_id, unsigned what, uint64_t new_cr_value)
{
    ExecuteCallback(ctx, tlb_cntrl, cpu_id, what, new_cr_value);
}

void
cache_cntrl_cb(context_t* ctx, uint32_t cpu_id, unsigned what)
{
    ExecuteCallback(ctx, cache_cntrl, cpu_id, what);
}

void
prefetch_hint_cb(context_t* ctx, uint32_t cpu_id, unsigned what, unsigned seg, uint64_t offset)
{
    ExecuteCallback(ctx, prefetch_hint, cpu_id, what, seg, offset);
}

void
wrmsr_cb(context_t* ctx, uint32_t cpu_id, unsigned msr, uint64_t value)
{
    ExecuteCallback(ctx, wrmsr, cpu_id, msr, value);
}

void
repeat_iteration_cb(context_t* ctx, uint32_t cpu_id, void* insn)
{
    ExecuteCallback(ctx, repeat_iteration, cpu_id, insn);
}

void
lin_access_cb(context_t* ctx, uint32_t cpu_id, uint64_t lin, uint64_t phy, uintptr_t len, uint32_t rw, uint32_t access)
{
    ExecuteCallback(ctx, lin_access, cpu_id, lin, phy, len, rw, access);
}

void
phy_access_cb(context_t* ctx, uint32_t cpu_id, uint64_t lin, uintptr_t phy, uint32_t len, uint32_t rw)
{
    ExecuteCallback(ctx, phy_access, cpu_id, lin, phy, len, rw);
}

void
inp_cb(context_t* ctx, uint16_t cpu_id, uintptr_t len)
{
    ExecuteCallback(ctx, inp, cpu_id, len);
}

void
inp2_cb(context_t* ctx, uint16_t cpu_id, uintptr_t len, unsigned val)
{
    ExecuteCallback(ctx, inp2, cpu_id, len, val);
}

void
outp_cb(context_t* ctx, uint16_t cpu_id, uintptr_t len, unsigned val)
{
    ExecuteCallback(ctx, outp, cpu_id, len, val);
}

void
opcode_cb(context_t* ctx, uint32_t cpu_id, void* insn, uint8_t* opcode, uintptr_t len, bool is32, bool is64)
{
    ExecuteCallback(ctx, opcode, cpu_id, insn, opcode, len, is32, is64);
}

void
exception_cb(context_t* ctx, uint32_t cpu_id, unsigned vector, unsigned error_code)
{
    ExecuteCallback(ctx, exception, cpu_id, vector, error_code);
}


}; // namespace BochsCPU::Callbacks