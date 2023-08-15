#include <nanobind/nanobind.h>
#include <nanobind/stl/array.h>
#include <nanobind/stl/function.h>
#include <nanobind/stl/list.h>
#include <nanobind/stl/optional.h>
#include <nanobind/stl/pair.h>
#include <nanobind/stl/vector.h>
#include <windows.h>

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

    m.def("PageSize", &BochsCPU::Memory::PageSize);

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
AlignPageToPage(uint64_t va)
{
    return va & ~0xfff;
}


//
// shamelessly ported from yrp's rust implem, because it was late and I wanted to finish
// kudos to him
//

PageMapLevel4Table::~PageMapLevel4Table()
{
    for ( auto addr : m_AllocatedPages )
    {
        (void)::VirtualFree((LPVOID)addr, 0, MEM_RELEASE);
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
        Entries[idx] = std::make_shared<PageDirectoryPointerTable>();

    auto pdpe = Entries.at(idx);
    pdpe->Flags.set((int)PageDirectoryPointerTable::Flag::Present);
    pdpe->Flags.set((int)PageDirectoryPointerTable::Flag::User);

    if ( type == 1 ) // RW
        pdpe->Flags.set((int)PageDirectoryPointerTable::Flag::Writable);


    // L3 insertion
    idx = PageDirectoryPointerTableIndex(va);
    if ( !pdpe->Entries[idx] )
        pdpe->Entries[idx] = std::make_shared<PageDirectory>();

    auto pde = pdpe->Entries.at(idx);
    pde->Flags.set((int)PageDirectoryPointerTable::Flag::Present);
    pde->Flags.set((int)PageDirectoryPointerTable::Flag::User);

    if ( type == 1 ) // RW
        pde->Flags.set((int)PageDirectoryPointerTable::Flag::Writable);


    // L2 insertion
    idx = PageDirectoryIndex(va);
    if ( !pde->Entries[idx] )
        pde->Entries[idx] = std::make_shared<PageTable>();

    auto pte = pde->Entries.at(idx);
    pte->Flags.set((int)PageTable::Flag::Present);
    pte->Flags.set((int)PageTable::Flag::User);

    if ( type == 1 ) // RW
        pte->Flags.set((int)PageDirectoryPointerTable::Flag::Writable);


    // L1 insertion
    idx = PageTableIndex(va);
    if ( !pte->Entries[idx] )
        pte->Entries[idx] = std::make_shared<PageTableEntry>();

    auto page = pte->Entries.at(idx);
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
    auto AllocatePage = [PageSize, &CurrentPA]() -> std::pair<uint64_t, uint64_t>
    {
        auto h = ::VirtualAlloc(nullptr, PageSize, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE);
        if ( !h )
            throw std::bad_alloc();

        uint64_t pa {CurrentPA};
        CurrentPA += PageSize;
        return {(uint64_t)h, pa};
    };

    const size_t view_size = PageSize / sizeof(uint64_t);
    const auto mapped_pml4 = AllocatePage();
    std::span<uint64_t> mapped_pml4_view {(uint64_t*)mapped_pml4.first, view_size};

    for ( int i = -1; auto const& pdpt : this->Entries )
    {
        i++;

        if ( !pdpt )
            continue;

        if ( !pdpt->Flags.test((int)PageDirectoryPointerTable::Flag::Present) )
            continue;

        auto mapped_pdpt = AllocatePage();
        std::span<uint64_t> mapped_pdpt_view {(uint64_t*)mapped_pdpt.first, view_size};

        for ( int j = -1; auto const& pd : pdpt->Entries )
        {
            j++;

            if ( !pd )
                continue;

            if ( !pd->Flags.test((int)PageDirectory::Flag::Present) )
                continue;

            auto mapped_pd = AllocatePage();
            std::span<uint64_t> mapped_pd_view {(uint64_t*)mapped_pd.first, view_size};

            for ( int k = -1; auto const& pt : pd->Entries )
            {
                k++;

                if ( !pt )
                    continue;

                if ( !pt->Flags.test((int)PageTable::Flag::Present) )
                    continue;

                auto mapped_pt = AllocatePage();
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


    //
    // Keep track of the allocated pages for deletion
    //
    for ( auto const& entry : mapped_locations )
    {
        m_AllocatedPages.push_back(entry.first);
    }

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