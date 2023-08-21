#include <array>
#include <bitset>
#include <functional>
#include <memory>
#include <optional>
#include <utility>
#include <vector>

#if defined(_WIN32)
#include <windows.h>
#elif defined(linux) || defined(__linux)
#include <sys/mman.h>
#elif defined(__APPLE__)
#include <sys/mman.h>
#else
#error Not supported
#endif // _WIN32

#include "bochscpu/bochscpu.hpp"

// #define DEBUG

#ifdef DEBUG
#define GEN_FMT "[%s::%d] "
#define dbg(fmt, ...) ::printf(GEN_FMT fmt "\n", __FUNCTION__, __LINE__, __VA_ARGS__)
#else
#define dbg(fmt, ...)
#endif // DEBUG

//
// Some missing defines
//

// For bx_instr_tlb_cntrl
#define BX_INSTR_MOV_CR0 10
#define BX_INSTR_MOV_CR3 11
#define BX_INSTR_MOV_CR4 12
#define BX_INSTR_TASK_SWITCH 13
#define BX_INSTR_CONTEXT_SWITCH 14 /* VMM and SMM enter/exit */
#define BX_INSTR_INVLPG 15
#define BX_INSTR_INVEPT 16
#define BX_INSTR_INVVPID 17
#define BX_INSTR_INVPCID 18

// For bx_instr_cache_cntrl
#define BX_INSTR_INVD 10
#define BX_INSTR_WBINVD 11

// For bx_instr_prefetch_hint (what)
#define BX_INSTR_PREFETCH_NTA 00
#define BX_INSTR_PREFETCH_T0 01
#define BX_INSTR_PREFETCH_T1 02
#define BX_INSTR_PREFETCH_T2 03


namespace BochsCPU
{
///
/// @brief Src https://github.com/lubomyr/bochs/blob/8e0b9abcd81cd24d4d9c68f7fdef2f53bc180d33/cpu/cpu.h#L306
///
///
enum class BochsException : uint32_t
{
    BX_DE_EXCEPTION = 0, // Divide Error (fault)
    BX_DB_EXCEPTION = 1, // Debug (fault/trap)
    BX_BP_EXCEPTION = 3, // Breakpoint (trap)
    BX_OF_EXCEPTION = 4, // Overflow (trap)
    BX_BR_EXCEPTION = 5, // BOUND (fault)
    BX_UD_EXCEPTION = 6,
    BX_NM_EXCEPTION = 7,
    BX_DF_EXCEPTION = 8,
    BX_TS_EXCEPTION = 10,
    BX_NP_EXCEPTION = 11,
    BX_SS_EXCEPTION = 12,
    BX_GP_EXCEPTION = 13,
    BX_PF_EXCEPTION = 14,
    BX_MF_EXCEPTION = 16,
    BX_AC_EXCEPTION = 17,
    BX_MC_EXCEPTION = 18,
    BX_XM_EXCEPTION = 19,
    BX_VE_EXCEPTION = 20,
    BX_CP_EXCEPTION = 21 // Control Protection (fault)
};

enum class InstructionType : uint32_t
{
    BX_INSTR_IS_JMP                 = BX_INSTR_IS_JMP,
    BOCHSCPU_INSTR_IS_JMP_INDIRECT  = BOCHSCPU_INSTR_IS_JMP_INDIRECT,
    BOCHSCPU_INSTR_IS_CALL          = BOCHSCPU_INSTR_IS_CALL,
    BOCHSCPU_INSTR_IS_CALL_INDIRECT = BOCHSCPU_INSTR_IS_CALL_INDIRECT,
    BOCHSCPU_INSTR_IS_RET           = BOCHSCPU_INSTR_IS_RET,
    BOCHSCPU_INSTR_IS_IRET          = BOCHSCPU_INSTR_IS_IRET,
    BOCHSCPU_INSTR_IS_INT           = BOCHSCPU_INSTR_IS_INT,
    BOCHSCPU_INSTR_IS_SYSCALL       = BOCHSCPU_INSTR_IS_SYSCALL,
    BOCHSCPU_INSTR_IS_SYSRET        = BOCHSCPU_INSTR_IS_SYSRET,
    BOCHSCPU_INSTR_IS_SYSENTER      = BOCHSCPU_INSTR_IS_SYSENTER,
    BOCHSCPU_INSTR_IS_SYSEXIT       = BOCHSCPU_INSTR_IS_SYSEXIT,
};


enum class HookType : uint32_t
{
    BOCHSCPU_HOOK_MEM_READ          = BOCHSCPU_HOOK_MEM_READ,
    BOCHSCPU_HOOK_MEM_WRITE         = BOCHSCPU_HOOK_MEM_WRITE,
    BOCHSCPU_HOOK_MEM_EXECUTE       = BOCHSCPU_HOOK_MEM_EXECUTE,
    BOCHSCPU_HOOK_MEM_RW            = BOCHSCPU_HOOK_MEM_RW,
    BOCHSCPU_HOOK_TLB_CR0           = BOCHSCPU_HOOK_TLB_CR0,
    BOCHSCPU_HOOK_TLB_CR3           = BOCHSCPU_HOOK_TLB_CR3,
    BOCHSCPU_HOOK_TLB_CR4           = BOCHSCPU_HOOK_TLB_CR4,
    BOCHSCPU_HOOK_TLB_TASKSWITCH    = BOCHSCPU_HOOK_TLB_TASKSWITCH,
    BOCHSCPU_HOOK_TLB_CONTEXTSWITCH = BOCHSCPU_HOOK_TLB_CONTEXTSWITCH,
    BOCHSCPU_HOOK_TLB_INVLPG        = BOCHSCPU_HOOK_TLB_INVLPG,
    BOCHSCPU_HOOK_TLB_INVEPT        = BOCHSCPU_HOOK_TLB_INVEPT,
    BOCHSCPU_HOOK_TLB_INVVPID       = BOCHSCPU_HOOK_TLB_INVVPID,
    BOCHSCPU_HOOK_TLB_INVPCID       = BOCHSCPU_HOOK_TLB_INVPCID,
};


enum class OpcodeOperationType
{
    BOCHSCPU_OPCODE_ERROR    = BOCHSCPU_OPCODE_ERROR,
    BOCHSCPU_OPCODE_INSERTED = BOCHSCPU_OPCODE_INSERTED,
};

///
/// @brief https://github.com/lubomyr/bochs/blob/8e0b9abcd81cd24d4d9c68f7fdef2f53bc180d33/cpu/cpu.h#L336
///
///
enum class BochsCpuMode : uint32_t
{
    BX_MODE_IA32_REAL      = 0, // CR0.PE=0                |
    BX_MODE_IA32_V8086     = 1, // CR0.PE=1, EFLAGS.VM=1   | EFER.LMA=0
    BX_MODE_IA32_PROTECTED = 2, // CR0.PE=1, EFLAGS.VM=0   |
    BX_MODE_LONG_COMPAT    = 3, // EFER.LMA = 1, CR0.PE=1, CS.L=0
    BX_MODE_LONG_64        = 4  // EFER.LMA = 1, CR0.PE=1, CS.L=1
};


namespace Callbacks
{
namespace Memory
{
void
missing_page_cb(uint64_t gpa);
} // namespace Memory

void
before_execution_cb(context_t* ctx, uint32_t cpu_id, void* insn);

void
after_execution_cb(context_t* ctx, uint32_t cpu_id, void* insn);

void
reset_cb(context_t* ctx, uint32_t cpu_id, unsigned int type);

void
hlt_cb(context_t* ctx, uint32_t cpu_id);

void
mwait_cb(context_t* ctx, uint32_t cpu_id, uint64_t addr, uintptr_t len, uint32_t flags);

void
cnear_branch_taken_cb(context_t* ctx, uint32_t cpu_id, uint64_t branch_eip, uint64_t new_branch_eip);

void
cnear_branch_not_taken_cb(context_t* ctx, uint32_t cpu_id, uint64_t branch_eip, uint64_t new_branch_eip);

void
ucnear_branch_cb(context_t* ctx, uint32_t cpu_id, unsigned what, uint64_t branch_eip, uint64_t new_eip);

void
far_branch_cb(context_t* ctx, uint32_t cpu_id, uint32_t, uint16_t, uint64_t, uint16_t, uint64_t);

void
vmexit_cb(context_t* ctx, uint32_t cpu_id, uint32_t, uint64_t);

void
interrupt_cb(context_t* ctx, uint32_t cpu_id, unsigned);

void
hw_interrupt_cb(context_t* ctx, uint32_t cpu_id, unsigned, uint16_t, uint64_t);

void
clflush_cb(context_t* ctx, uint32_t cpu_id, uint64_t, uint64_t);

void
tlb_cntrl_cb(context_t* ctx, uint32_t cpu_id, unsigned, uint64_t);

void
cache_cntrl_cb(context_t* ctx, uint32_t cpu_id, unsigned);

void
prefetch_hint_cb(context_t* ctx, uint32_t cpu_id, unsigned, unsigned, uint64_t);

void
wrmsr_cb(context_t* ctx, uint32_t cpu_id, unsigned, uint64_t);

void
repeat_iteration_cb(context_t* ctx, uint32_t cpu_id, void*);

void
lin_access_cb(context_t* ctx, uint32_t cpu_id, uint64_t, uint64_t, uintptr_t, uint32_t, uint32_t);

void
phy_access_cb(context_t* ctx, uint32_t cpu_id, uint64_t, uintptr_t, uint32_t, uint32_t);

void
inp_cb(context_t* ctx, uint16_t cpu_id, uintptr_t);

void
inp2_cb(context_t* ctx, uint16_t cpu_id, uintptr_t, unsigned);

void
outp_cb(context_t* ctx, uint16_t cpu_id, uintptr_t, unsigned);

void
opcode_cb(context_t* ctx, uint32_t cpu_id, void*, uint8_t*, uintptr_t, bool, bool);

void
exception_cb(context_t* ctx, uint32_t cpu_id, unsigned vector, unsigned error_code);

} // namespace Callbacks


namespace Cpu
{

enum class ControlRegisterFlag : uint64_t
{
    /// CR0 - - AMD Manual Vol2 - 3.1.1
    PG = 31, // Paging R/W
    CD = 30, // Cache Disable R/W
    NW = 29, // Not Writethrough R/W
    AM = 18, // Alignment Mask R/W
    WP = 16, // Write Protect R/W
    NE = 5,  // Numeric Error R/W
    ET = 4,  // Extension Type R
    TS = 3,  // Task Switched R/W
    EM = 2,  // Emulation R/W
    MP = 1,  // Monitor Coprocessor R/W
    PE = 0,  // Protection Enabled R/W


    /// CR4 - - AMD Manual Vol2 - 3.7.1
    OSXSAVE    = 18, // XSAVE and Processor Extended States Enable Bit R/W
    FSGSBASE   = 16, // Enable RDFSBASE, RDGSBASE, WRFSBASE, and WRGSBASE instructions R/W
    OSXMMEXCPT = 10, // Operating System Unmasked Exception Support R/W
    OSFXSR     = 9,  // Operating System FXSAVE/FXRSTOR Support R/W
    PCE        = 8,  // Performance-Monitoring Counter Enable R/W
    PGE        = 7,  // Page-Global Enable R/W
    MCE        = 6,  // Machine Check Enable R/W
    PAE        = 5,  // Physical-Address Extension R/W
    PSE        = 4,  // Page Size Extensions R/W
    DE         = 3,  // Debugging Extensions R/W
    TSD        = 2,  // Time Stamp Disable R/W
    PVI        = 1,  // Protected-Mode Virtual Interrupts R/W
    VME        = 0,  // Virtual-8086 Mode Extensions R/W
};

enum class FlagRegisterFlag : uint64_t
{
    // RFLAGS - AMD Manual Vol2 - 3.8
    ID        = 21, // ID Flag R/W
    VIP       = 20, // Virtual Interrupt Pending R/W
    VIF       = 19, // Virtual Interrupt Flag R/W
    AC        = 18, // Alignment Check R/W
    VM        = 17, // Virtual-8086 Mode R/W
    RF        = 16, // Resume Flag R/W
    Reserved4 = 15, // Read as Zero
    NT        = 14, // Nested Task R/W
    IOPL2     = 13, // IOPL I/O Privilege Level R/W
    IOPL1     = 12, // IOPL I/O Privilege Level R/W
    OF        = 11, // Overflow Flag R/W
    DF        = 10, // Direction Flag R/W
    IF        = 9,  // Interrupt Flag R/W
    TF        = 8,  // Trap Flag R/W
    SF        = 7,  // Sign Flag R/W
    ZF        = 6,  // Zero Flag R/W
    Reserved3 = 5,  // Read as Zero
    AF        = 4,  // Auxiliary Flag R/W
    Reserved2 = 3,  // Read as Zero
    PF        = 2,  // Parity Flag R/W
    Reserved1 = 1,  // Read as One
    CF        = 0,  // Carry Flag R/W
};

enum class FeatureRegisterFlag : uint64_t
{
    TCE   = 15, // Translation Cache Extension R/W
    FFXSR = 14, // Fast FXSAVE/FXRSTOR R/W
    LMSLE = 13, // Long Mode Segment Limit Enable R/W
    SVME  = 12, // Secure Virtual Machine Enable R/W
    NXE   = 11, // No-Execute Enable R/W
    LMA   = 10, // Long Mode Active R/W
    LME   = 8,  // Long Mode Enable R/W
    SCE   = 0,  // System Call Extensions R/W
};

struct ControlRegister : std::bitset<64>
{
};


struct FlagRegister : std::bitset<64>
{
    FlagRegister()
    {
        set((int)FlagRegisterFlag::Reserved1, true);
    }
};

struct FeatureRegister : std::bitset<64>
{
};


static uint32_t g_sessionId {0};

struct CPU
{
    CPU()
    {
        this->id  = g_sessionId++;
        this->cpu = ::bochscpu_cpu_new(this->id);
        if ( !this->cpu )
            throw std::runtime_error("Invalid CPU ID");
        dbg("Created CPU#%lu", this->id);
    }

    ~CPU()
    {
        ::bochscpu_cpu_delete(this->cpu);
    }

    uint32_t id {0};
    bochscpu_cpu_t cpu {};
};
} // namespace Cpu


namespace Memory
{

enum class Access : uint32_t
{
    Read    = (uint32_t)BochsCPU::HookType::BOCHSCPU_HOOK_MEM_READ,
    Write   = (uint32_t)BochsCPU::HookType::BOCHSCPU_HOOK_MEM_WRITE,
    Execute = (uint32_t)BochsCPU::HookType::BOCHSCPU_HOOK_MEM_EXECUTE,
};

uintptr_t
PageSize();

uint64_t
AlignAddressToPage(uint64_t va);

uint64_t
AllocatePage();

bool
FreePage(uint64_t addr);


//
// @ref AMD Programmer's Manual Volume 2, Figure 5.17
//

struct PageTableEntry
{
    enum class Flag
    {
        Present        = 0,
        Writable       = 1,
        User           = 2,
        WriteThrough   = 3,
        CacheDisabled  = 4,
        Accessed       = 5,
        Dirty          = 6,
        AttributeTable = 7,
        Global         = 8,
        NX             = 63,
    };

    uint64_t Address {};
    std::bitset<64> Flags {};

    PageTableEntry() = default;
};

struct PageTable
{
    enum class Flag
    {
        Present       = 0,
        Writable      = 1,
        User          = 2,
        WriteThrough  = 3,
        CacheDisabled = 4,
        Accessed      = 5,
        Size          = 7,
        NX            = 63,
    };

    std::array<std::unique_ptr<PageTableEntry>, 512> Entries {};
    std::bitset<64> Flags {};

    PageTable() = default;
};

struct PageDirectory
{
    enum class Flag
    {
        Present       = 0,
        Writable      = 1,
        User          = 2,
        WriteThrough  = 3,
        CacheDisabled = 4,
        Accessed      = 5,
        Size          = 7,
        NX            = 63,
    };

    std::array<std::unique_ptr<PageTable>, 512> Entries {};
    std::bitset<64> Flags {};

    PageDirectory() = default;
};

struct PageDirectoryPointerTable
{
    enum class Flag : int
    {
        Present       = 0,
        Writable      = 1,
        User          = 2,
        WriteThrough  = 3,
        CacheDisabled = 4,
        Accessed      = 5,
        Size          = 7,
        NX            = 63,
    };

    std::array<std::unique_ptr<PageDirectory>, 512> Entries {};
    std::bitset<64> Flags {};

    PageDirectoryPointerTable() = default;
};


class PageMapLevel4Table
{
public:
    enum class Flag : int
    {
        Present       = 0,
        Writable      = 1,
        User          = 2,
        WriteThrough  = 3,
        CacheDisabled = 4,
        Accessed      = 5,
        Size          = 7,
        NX            = 63,
    };

    PageMapLevel4Table() = default;

    ~PageMapLevel4Table();

    std::optional<uint64_t>
    Translate(uint64_t va);

    void
    Insert(uint64_t va, uint64_t pa, int type);


    std::vector<std::pair<uint64_t, uint64_t>>
    Commit(uint64_t BasePA);

    void
    Decommit();

public: // members
    std::array<std::unique_ptr<PageDirectoryPointerTable>, 512> Entries {};
    std::bitset<64> Flags {};


private:
    uint64_t
    PageMapLevel4Index(uint64_t va);

    uint64_t
    PageDirectoryPointerTableIndex(uint64_t va);

    uint64_t
    PageDirectoryIndex(uint64_t va);

    uint64_t
    PageTableIndex(uint64_t va);

    uint64_t
    PageOffset(uint64_t va);

private:
    std::vector<uint64_t> m_AllocatedPages {};
};

static inline std::unique_ptr<std::function<void(uint64_t)>> missing_page_handler;

static void
missing_page_cb(uint64_t gpa)
{
    dbg("missing gpa=%#llx", gpa);
    (*missing_page_handler)(gpa);
}
} // namespace Memory


struct Session
{
    Session() : cpu()
    {
        ::bochscpu_mem_missing_page(BochsCPU::Memory::missing_page_cb);
        BochsCPU::Memory::missing_page_handler =
            std::unique_ptr<std::function<void(uint64_t)>>(&this->missing_page_handler);
    }

    ~Session()
    {
        BochsCPU::Memory::missing_page_handler.release();
    }

    std::function<void(uint64_t)> missing_page_handler;
    BochsCPU::Cpu::CPU cpu {};
};


struct Hook
{
    void* ctx {nullptr};
    std::function<void(Session*, uint32_t, void*)> before_execution;
    std::function<void(Session*, uint32_t, void*)> after_execution;
    std::function<void(Session*, uint32_t, unsigned int)> reset;
    std::function<void(Session*, uint32_t)> hlt;
    std::function<void(Session*, uint32_t, uint64_t, uintptr_t, uint32_t)> mwait;
    std::function<void(Session*, uint32_t, uint64_t, uint64_t)> cnear_branch_taken;
    std::function<void(Session*, uint32_t, uint64_t, uint64_t)> cnear_branch_not_taken;
    std::function<void(Session*, uint32_t, unsigned, uint64_t, uint64_t)> ucnear_branch;
    std::function<void(Session*, uint32_t, uint32_t, uint16_t, uint64_t, uint16_t, uint64_t)> far_branch;
    std::function<void(Session*, uint32_t, uint32_t, uint64_t)> vmexit;
    std::function<void(Session*, uint32_t, unsigned)> interrupt;
    std::function<void(Session*, uint32_t, unsigned, uint16_t, uint64_t)> hw_interrupt;
    std::function<void(Session*, uint32_t, uint64_t, uint64_t)> clflush;
    std::function<void(Session*, uint32_t, unsigned, uint64_t)> tlb_cntrl;
    std::function<void(Session*, uint32_t, unsigned)> cache_cntrl;
    std::function<void(Session*, uint32_t, unsigned, unsigned, uint64_t)> prefetch_hint;
    std::function<void(Session*, uint32_t, unsigned, uint64_t)> wrmsr;
    std::function<void(Session*, uint32_t, void*)> repeat_iteration;
    std::function<void(Session*, uint32_t, uint64_t, uint64_t, uintptr_t, uint32_t, uint32_t)> lin_access;
    std::function<void(Session*, uint32_t, uint64_t, uint64_t, uintptr_t, unsigned)> phy_access;
    std::function<void(Session*, uint16_t, uintptr_t)> inp;
    std::function<void(Session*, uint16_t, uintptr_t, unsigned)> inp2;
    std::function<void(Session*, uint16_t, uintptr_t, unsigned)> outp;
    std::function<void(Session*, uint32_t, void*, uint8_t*, uintptr_t, bool, bool)> opcode;
    std::function<void(Session*, uint32_t, unsigned, unsigned)> exception;
};


} // namespace BochsCPU