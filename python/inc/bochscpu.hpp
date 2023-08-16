#include <array>
#include <bitset>
#include <functional>
#include <memory>
#include <optional>
#include <utility>
#include <vector>

#include "bochscpu/bochscpu.hpp"

#define DEBUG

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

struct Hook
{
    void* ctx {nullptr};
    std::function<void(context_t*, uint32_t, void*)> before_execution;
    std::function<void(context_t*, uint32_t, void*)> after_execution;
    std::function<void(context_t*, uint32_t, unsigned int)> reset;
    std::function<void(context_t*, uint32_t)> hlt;
    std::function<void(context_t*, uint32_t, uint64_t, uintptr_t, uint32_t)> mwait;
    std::function<void(context_t*, uint32_t, uint64_t, uint64_t)> cnear_branch_taken;
    std::function<void(context_t*, uint32_t, uint64_t, uint64_t)> cnear_branch_not_taken;
    std::function<void(context_t*, uint32_t, unsigned, uint64_t, uint64_t)> ucnear_branch;
    std::function<void(context_t*, uint32_t, uint32_t, uint16_t, uint64_t, uint16_t, uint64_t)> far_branch;
    std::function<void(context_t*, uint32_t, uint32_t, uint64_t)> vmexit;
    std::function<void(context_t*, uint32_t, unsigned)> interrupt;
    std::function<void(context_t*, uint32_t, unsigned, uint16_t, uint64_t)> hw_interrupt;
    std::function<void(context_t*, uint32_t, uint64_t, uint64_t)> clflush;
    std::function<void(context_t*, uint32_t, unsigned, uint64_t)> tlb_cntrl;
    std::function<void(context_t*, uint32_t, unsigned)> cache_cntrl;
    std::function<void(context_t*, uint32_t, unsigned, unsigned, uint64_t)> prefetch_hint;
    std::function<void(context_t*, uint32_t, unsigned, uint64_t)> wrmsr;
    std::function<void(context_t*, uint32_t, void*)> repeat_iteration;
    std::function<void(context_t*, uint32_t, uint64_t, uint64_t, uintptr_t, uint32_t, uint32_t)> lin_access;
    std::function<void(context_t*, uint32_t, uint64_t, uint64_t, uintptr_t, unsigned)> phy_access;
    std::function<void(context_t*, uint16_t, uintptr_t)> inp;
    std::function<void(context_t*, uint16_t, uintptr_t, unsigned)> inp2;
    std::function<void(context_t*, uint16_t, uintptr_t, unsigned)> outp;
    std::function<void(context_t*, uint32_t, void*, uint8_t*, uintptr_t, bool, bool)> opcode;
    std::function<void(context_t*, uint32_t, unsigned, unsigned)> exception;
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

struct ControlRegister : std::bitset<64>
{
};

enum class ControlRegisterFlag : uint64_t
{
    /// CR0 - 3.1.1
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


    /// CR4 - 3.7.1
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

} // namespace Cpu


namespace Memory
{

uintptr_t
PageSize();

uint64_t
AlignPageToPage(uint64_t va);


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

} // namespace Memory

static inline std::unique_ptr<std::function<void(uint64_t)>> missing_page_handler;

static void
missing_page_cb(uint64_t gpa)
{
    dbg("missing gpa=%#llx", gpa);
    (*missing_page_handler)(gpa);
}

struct Session
{
    Session()
    {
        ::bochscpu_mem_missing_page(BochsCPU::missing_page_cb);
        BochsCPU::missing_page_handler = std::unique_ptr<std::function<void(uint64_t)>>(&this->missing_page_handler);
        // cpu                            = ::bochscpu_cpu_new(0);
    }

    ~Session()
    {
        // ::bochscpu_cpu_delete(cpu);
        BochsCPU::missing_page_handler.release();
    }

    std::function<void(uint64_t)> missing_page_handler;
    bochscpu_cpu_t cpu {};
};

} // namespace BochsCPU