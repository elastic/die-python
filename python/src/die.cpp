#include "die.hpp"

#include <nanobind/nanobind.h>
#include <nanobind/stl/filesystem.h>
#include <nanobind/stl/optional.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>

#include <array>
#include <filesystem>
#include <functional>
#include <memory>
#include <string_view>

namespace nb = nanobind;
using namespace nb::literals;


namespace DIE
{
std::optional<std::string>
ScanFileA(std::string& pszFileName, uint32_t nFlags, std::string& pszDatabase)
{
    auto res = ::DIE_ScanFileA(pszFileName.data(), static_cast<int>(nFlags), pszDatabase.data());
    if ( res == nullptr )
    {
        return std::nullopt;
    }

    auto const res_str = std::string(res);
    ::DIE_FreeMemoryA(res);
    return res_str;
}

std::optional<std::string>
ScanFileExA(std::string& pszFileName, uint32_t nFlags)
{
    auto res = ::DIE_ScanFileExA(pszFileName.data(), static_cast<int>(nFlags));
    if ( res == nullptr )
    {
        return std::nullopt;
    }

    auto const res_str = std::string(res);
    ::DIE_FreeMemoryA(res);
    return res_str;
}

std::optional<std::string>
ScanMemoryA(std::vector<uint8_t>& memory, uint32_t flags, std::string& database)
{
    char* pMemory     = (char*)memory.data();
    int nMemorySize   = static_cast<int>(memory.size());
    int nFlags        = static_cast<int>(flags);
    char* pszDatabase = database.data();
    auto res          = ::DIE_ScanMemoryA(pMemory, nMemorySize, nFlags, pszDatabase);
    if ( res == nullptr )
    {
        return std::nullopt;
    }

    auto const res_str = std::string(res);
    ::DIE_FreeMemoryA(res);
    return res_str;
}

std::optional<std::string>
ScanMemoryExA(std::vector<uint8_t>& memory, uint32_t flags)
{
    char* pMemory   = (char*)memory.data();
    int nMemorySize = static_cast<int>(memory.size());
    int nFlags      = static_cast<int>(flags);
    auto res        = ::DIE_ScanMemoryExA(pMemory, nMemorySize, nFlags);
    if ( res == nullptr )
    {
        return std::nullopt;
    }

    auto const res_str = std::string(res);
    ::DIE_FreeMemoryA(res);
    return res_str;
}

int32_t
LoadDatabaseA(std::string& pszDatabase)
{
    return ::DIE_LoadDatabaseA(pszDatabase.data());
}

#ifdef _WIN32
int
VB_ScanFile(
    std::wstring& pwszFileName,
    uint32_t nFlags,
    std::wstring& pwszDatabase,
    std::wstring& pwszBuffer,
    uint32_t nBufferSize)
{
    return ::DIE_VB_ScanFile(
        pwszFileName.data(),
        static_cast<int>(nFlags),
        pwszDatabase.data(),
        pwszBuffer.data(),
        static_cast<int>(nBufferSize));
}
#endif // _WIN32

} // namespace DIE


NB_MODULE(_die, m)
{
    nb::enum_<DIE::DieFlags>(m, "DieFlags")
        .value("Deepscan", DIE::DieFlags::Deepscan)
        .value("HeuristicScan", DIE::DieFlags::HeuristicScan)
        .value("AlltypesScan", DIE::DieFlags::AlltypesScan)
        .value("RecursiveScan", DIE::DieFlags::RecursiveScan)
        .value("Verbose", DIE::DieFlags::Verbose)
        .value("ResultAsXml", DIE::DieFlags::ResultAsXml)
        .value("ResultAsJson", DIE::DieFlags::ResultAsJson)
        .value("ResultAsTsv", DIE::DieFlags::ResultAsTsv)
        .value("ResultAsCsv", DIE::DieFlags::ResultAsCsv)
        .export_values();

    m.doc()                  = "The native `die` module";
    m.attr("__version__")    = "0.3.1";
    m.attr("die_version")    = DIE_VERSION;
    m.attr("dielib_version") = DIELIB_VERSION;

    m.def("ScanFileA", DIE::ScanFileA, "filename"_a, "flags"_a, "database"_a, "Scan a file against known signatures");

    m.def("ScanFileExA", DIE::ScanFileExA, "filename"_a, "flags"_a, "Scan a file");

    m.def(
        "ScanMemoryA",
        DIE::ScanMemoryA,
        "memory"_a,
        "flags"_a,
        "database"_a,
        "Scan sequence of bytes against known signatures");

    m.def("ScanMemoryExA", DIE::ScanMemoryExA, "memory"_a, "flags"_a, "Scan sequence of bytes");

    m.def("LoadDatabaseA", DIE::LoadDatabaseA, "database"_a, "Load signature database");
}
