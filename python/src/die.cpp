#include "die.hpp"

#include <nanobind/nanobind.h>
#include <nanobind/stl/filesystem.h>
#include <nanobind/stl/optional.h>
#include <nanobind/stl/string.h>

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

std::optional<std::wstring>
ScanFileW(std::wstring& pwszFileName, uint32_t nFlags, std::wstring& pwszDatabase)
{
    auto res = ::DIE_ScanFileW(pwszFileName.data(), static_cast<int>(nFlags), pwszDatabase.data());
    if ( res == nullptr )
    {
        return std::nullopt;
    }

    ::DIE_FreeMemoryW(res);
    return std::wstring(res);
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
    m.attr("__version__")    = "0.3.0";
    m.attr("die_version")    = DIE_VERSION;
    m.attr("dielib_version") = DIELIB_VERSION;

    m.def("ScanFileA", DIE::ScanFileA, "pszFileName"_a, "nFlags"_a, "pszDatabase"_a, "Scan a file (ascii string)");
    m.def("ScanFileW", DIE::ScanFileW, "pwszFileName"_a, "nFlags"_a, "pszDatabase"_a, "Scan a file (unicode string)");
}
