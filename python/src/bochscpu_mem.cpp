#include <nanobind/nanobind.h>
#include <nanobind/stl/array.h>
#include <nanobind/stl/function.h>
#include <nanobind/stl/list.h>
#include <nanobind/stl/optional.h>
#include <nanobind/stl/pair.h>
#include <nanobind/stl/vector.h>

#include <span>

#include "bochscpu.hpp"

namespace nb = nanobind;
using namespace nb::literals;

///
/// @brief BochsCPU Memory submodule Python interface
///
void
bochscpu_memory_module(nb::module_& base_module)
{
    auto m = base_module.def_submodule("memory", "Memory module");

    nb::enum_<BochsCPU::Memory::Access>(m, "AccessType")
        .value("Read", BochsCPU::Memory::Access::Read)
        .value("Write", BochsCPU::Memory::Access::Write)
        .value("Execute", BochsCPU::Memory::Access::Execute);

    m.def("PageSize", &BochsCPU::Memory::PageSize);
    m.def("AlignAddressToPage", &BochsCPU::Memory::AlignAddressToPage);

    m.def(
        "page_insert",
        [](uint64_t gpa, uintptr_t hva)
        {
            dbg("mapping GPA=%#llx <-> HVA=%#llx", gpa, hva);
            ::bochscpu_mem_page_insert(gpa, (uint8_t*)hva);
        },
        "Map a GPA to a HVA");
    m.def("page_remove", &bochscpu_mem_page_remove, "gpa"_a);
    m.def(
        "phy_translate",
        [](const uint64_t gpa)
        {
            return (uintptr_t)(::bochscpu_mem_phy_translate(gpa));
        },
        "gpa"_a);
    m.def("virt_translate", &bochscpu_mem_virt_translate, "cr3"_a, "gva"_a);
    m.def(
        "phy_read",
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
        "phy_write",
        [](uint64_t gpa, std::vector<uint8_t> const& hva)
        {
            ::bochscpu_mem_phy_write(gpa, hva.data(), hva.size());
        },
        "gpa"_a,
        "hva"_a,
        "Write to GPA");
    m.def(
        "virt_write",
        [](uint64_t cr3, uint64_t gva, std::vector<uint8_t> const& hva)
        {
            return ::bochscpu_mem_virt_write(cr3, gva, hva.data(), hva.size()) == 0;
        },
        "cr3"_a,
        "gva"_a,
        "hva"_a,
        "Write to GVA");
    m.def(
        "virt_read",
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

    nb::class_<BochsCPU::Memory::PageMapLevel4Table>(m, "PageMapLevel4Table")
        .def(nb::init<>())
        .def("Translate", &BochsCPU::Memory::PageMapLevel4Table::Translate, "Translate a VA -> PA")
        .def("Insert", &BochsCPU::Memory::PageMapLevel4Table::Insert, "Associate the VA to PA")
        .def("Commit", &BochsCPU::Memory::PageMapLevel4Table::Commit, "Commit the layout of the tree to memory");
}

namespace BochsCPU::Memory
{


uintptr_t
PageSize()
{
    return 0x1000;
}


uint64_t
AlignAddressToPage(uint64_t va)
{
    return va & ~0xfff;
}


uint64_t
AllocatePage()
{
#if defined(_WIN32)
    return (uint64_t)::VirtualAlloc(nullptr, Memory::PageSize(), MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE);
#else
    return (uint64_t)::mmap(nullptr, Memory::PageSize(), PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
#endif // _WIN32
}


bool
FreePage(uint64_t addr)
{
#if defined(_WIN32)
    return ::VirtualFree((LPVOID)addr, 0, MEM_RELEASE) == TRUE;
#else
    return ::munmap((void*)addr, Memory::PageSize()) == 0;
#endif // _WIN32
}


//
// shamelessly ported from yrp's rust implem, because it was late and I wanted to finish
// kudos to him
//

PageMapLevel4Table::~PageMapLevel4Table()
{
    for ( auto addr : m_AllocatedPages )
    {
        FreePage(addr);
    }
}

std::optional<uint64_t>
PageMapLevel4Table::Translate(uint64_t va)
{
    // L4 -> L3
    auto& pdpe = Entries.at(PageMapLevel4Index(va));
    if ( !pdpe || !pdpe->Flags.test((int)PageDirectoryPointerTable::Flag::Present) )
        return std::nullopt;


    // L3 -> L2
    auto& pde = pdpe->Entries.at(PageDirectoryPointerTableIndex(va));
    if ( !pde || !pde->Flags.test((int)PageDirectory::Flag::Present) )
        return std::nullopt;


    // L2 -> L1
    auto& pte = pde->Entries.at(PageDirectoryIndex(va));
    if ( !pte || !pte->Flags.test((int)PageTable::Flag::Present) )
        return std::nullopt;


    // L1 -> PA
    auto& page = pte->Entries.at(PageTableIndex(va));
    if ( !page || !page->Flags.test((int)PageTableEntry::Flag::Present) )
        return std::nullopt;

    return page->Address;
}

void
PageMapLevel4Table::Insert(uint64_t va, uint64_t pa, int type)
{
    // L4 insertion
    uint64_t idx = PageMapLevel4Index(va);
    if ( !Entries[idx] )
        Entries[idx] = std::make_unique<PageDirectoryPointerTable>();

    auto& pdpe = Entries.at(idx);
    pdpe->Flags.set((int)PageDirectoryPointerTable::Flag::Present);
    pdpe->Flags.set((int)PageDirectoryPointerTable::Flag::User);

    if ( type == 1 ) // RW
        pdpe->Flags.set((int)PageDirectoryPointerTable::Flag::Writable);


    // L3 insertion
    idx = PageDirectoryPointerTableIndex(va);
    if ( !pdpe->Entries[idx] )
        pdpe->Entries[idx] = std::make_unique<PageDirectory>();

    auto& pde = pdpe->Entries.at(idx);
    pde->Flags.set((int)PageDirectoryPointerTable::Flag::Present);
    pde->Flags.set((int)PageDirectoryPointerTable::Flag::User);

    if ( type == 1 ) // RW
        pde->Flags.set((int)PageDirectoryPointerTable::Flag::Writable);


    // L2 insertion
    idx = PageDirectoryIndex(va);
    if ( !pde->Entries[idx] )
        pde->Entries[idx] = std::make_unique<PageTable>();

    auto& pte = pde->Entries.at(idx);
    pte->Flags.set((int)PageTable::Flag::Present);
    pte->Flags.set((int)PageTable::Flag::User);

    if ( type == 1 ) // RW
        pte->Flags.set((int)PageDirectoryPointerTable::Flag::Writable);


    // L1 insertion
    idx = PageTableIndex(va);
    if ( !pte->Entries[idx] )
        pte->Entries[idx] = std::make_unique<PageTableEntry>();

    auto& page = pte->Entries.at(idx);
    page->Flags.set((int)PageTableEntry::Flag::Present);
    page->Flags.set((int)PageTableEntry::Flag::User);

    if ( type == 1 ) // RW
        page->Flags.set((int)PageTableEntry::Flag::Writable);

    page->Address = pa;
}

std::vector<std::pair<uint64_t, uint64_t>>
PageMapLevel4Table::Commit(uint64_t BasePA)
{
    std::vector<std::pair<uint64_t, uint64_t>> mapped_locations;
    uint64_t PageSize = BochsCPU::Memory::PageSize();
    uint64_t CurrentPA {BasePA};

    // pair<HVA, GPA>
    auto AllocatePageAndPA = [this, PageSize, &CurrentPA]() -> std::pair<uint64_t, uint64_t>
    {
        auto h = BochsCPU::Memory::AllocatePage();
        if ( !h )
            throw std::bad_alloc();

        //
        // Keep track of the allocated pages for deletion
        //
        m_AllocatedPages.push_back(h);

        uint64_t pa {CurrentPA};
        CurrentPA += PageSize;
        return {h, pa};
    };

    const size_t view_size = PageSize / sizeof(uint64_t);
    const auto mapped_pml4 = AllocatePageAndPA();
    std::span<uint64_t> mapped_pml4_view {(uint64_t*)mapped_pml4.first, view_size};

    for ( int i = -1; auto const& pdpt : this->Entries )
    {
        i++;

        if ( !pdpt )
            continue;

        if ( !pdpt->Flags.test((int)PageDirectoryPointerTable::Flag::Present) )
            continue;

        auto mapped_pdpt = AllocatePageAndPA();
        std::span<uint64_t> mapped_pdpt_view {(uint64_t*)mapped_pdpt.first, view_size};

        for ( int j = -1; auto const& pd : pdpt->Entries )
        {
            j++;

            if ( !pd )
                continue;

            if ( !pd->Flags.test((int)PageDirectory::Flag::Present) )
                continue;

            auto mapped_pd = AllocatePageAndPA();
            std::span<uint64_t> mapped_pd_view {(uint64_t*)mapped_pd.first, view_size};

            for ( int k = -1; auto const& pt : pd->Entries )
            {
                k++;

                if ( !pt )
                    continue;

                if ( !pt->Flags.test((int)PageTable::Flag::Present) )
                    continue;

                auto mapped_pt = AllocatePageAndPA();
                std::span<uint64_t> mapped_pt_view {(uint64_t*)mapped_pt.first, view_size};

                for ( int l = -1; auto const& page : pt->Entries )
                {
                    l++;

                    if ( !page )
                        continue;

                    if ( !page->Flags.test((int)PageTableEntry::Flag::Present) )
                        continue;

                    mapped_pt_view[l] = page->Address | page->Flags.to_ulong();
                }

                mapped_pd_view[k] = mapped_pt.second | pt->Flags.to_ulong();
                mapped_locations.push_back(mapped_pt);
            }

            mapped_pdpt_view[j] = mapped_pd.second | pd->Flags.to_ulong();
            mapped_locations.push_back(mapped_pd);
        }

        mapped_pml4_view[i] = mapped_pdpt.second | pdpt->Flags.to_ulong();
        mapped_locations.push_back(mapped_pdpt);
    }

    mapped_locations.push_back(mapped_pml4);
    return mapped_locations;
}

uint64_t
PageMapLevel4Table::PageMapLevel4Index(uint64_t va)
{
    return (va >> (12 + (9 * 3))) & 0b1'1111'1111;
}

uint64_t
PageMapLevel4Table::PageDirectoryPointerTableIndex(uint64_t va)
{
    return (va >> (12 + (9 * 2))) & 0b1'1111'1111;
}

uint64_t
PageMapLevel4Table::PageDirectoryIndex(uint64_t va)
{
    return (va >> (12 + 9)) & 0b1'1111'1111;
}

uint64_t
PageMapLevel4Table::PageTableIndex(uint64_t va)
{
    return (va >> 12) & 0b1'1111'1111;
}

uint64_t
PageMapLevel4Table::PageOffset(uint64_t va)
{
    return va & 0xfff;
}

} // namespace BochsCPU::Memory