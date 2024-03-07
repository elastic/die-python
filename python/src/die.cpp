#include "die.hpp"

#include <nanobind/nanobind.h>
#include <nanobind/stl/optional.h>
#include <nanobind/stl/string.h>

#include <array>
#include <filesystem>
#include <functional>
#include <memory>
#include <string_view>

const std::filesystem::path SitePackagePath =
    "C:\\Users\\chris\\AppData\\Roaming\\Python\\Python312\\site-packages\\die";
const std::filesystem::path DieDll       = SitePackagePath / "die.dll";
const std::filesystem::path Qt5ScriptDll = SitePackagePath / "qt5script.dll";
const std::filesystem::path Qt5CoreDll   = SitePackagePath / "qt5core.dll";

namespace nb = nanobind;
using namespace nb::literals;

template<typename T, auto Deleter>
using GenericHandle = std::unique_ptr<
    T,
    decltype(
        [](T* h)
        {
            if ( h )
            {
                Deleter(h);
                h = nullptr;
            }
        })>;

#ifdef __linux__
using UniqueHandle = GenericHandle<FILE, ::fclose>;
using UniqueModule = GenericHandle<FILE, ::dlclose>;
#else
using UniqueHandle = GenericHandle<void, ::CloseHandle>;
using UniqueModule = GenericHandle<HINSTANCE__, [](auto x) {}>;
#endif // __linux__

using OriginalScanFileA_Sig   = char* (*)(char*, unsigned int, char*);
using OriginalScanFileW_Sig   = wchar_t* (*)(wchar_t* pwszFileName, unsigned int nFlags, wchar_t* pwszDatabase);
using OriginalFreeMemoryA_Sig = void (*)(char* pszString);
using OriginalFreeMemoryW_Sig = void (*)(char* pwszString);
using OriginalVB_ScanFile_Sig =
    int (*)(wchar_t* pwszFileName, unsigned int nFlags, wchar_t* pwszDatabase, wchar_t* pwszBuffer, int nBufferSize);

namespace DIE
{

std::array<void*, 5> __FunctionPointers;

void
Init()
{
    if ( __FunctionPointers[0] != nullptr ) [[likely]]
    {
        return;
    }

    const UniqueModule hQtCoreMod {::LoadLibraryA(Qt5CoreDll.string().c_str())};
    const UniqueModule hQtScriptMod {::LoadLibraryA(Qt5ScriptDll.string().c_str())};
    const UniqueModule hDieMod {::LoadLibraryA(DieDll.string().c_str())};
    if ( !hDieMod )
    {
        printf("[CRITICAL] LoadLibraryA() failed, GLE=%#x\n", ::GetLastError());
        return;
    }

    __FunctionPointers[0] = static_cast<void*>(::GetProcAddress(hDieMod.get(), "DIE_ScanFileA"));
    __FunctionPointers[1] = static_cast<void*>(::GetProcAddress(hDieMod.get(), "DIE_ScanFileW"));
    __FunctionPointers[2] = static_cast<void*>(::GetProcAddress(hDieMod.get(), "DIE_FreeMemoryA"));
    __FunctionPointers[3] = static_cast<void*>(::GetProcAddress(hDieMod.get(), "DIE_FreeMemoryW"));
    __FunctionPointers[4] = static_cast<void*>(::GetProcAddress(hDieMod.get(), "DIE_VB_ScanFile"));
}

void
Check(int index)
{
    if ( !__FunctionPointers[index] ) [[unlikely]]
    {
        Init();

        if ( !__FunctionPointers[index] )
        {
            throw std::runtime_error("Pointer initialization failed");
        }
    }
}

std::optional<std::string>
ScanFileA(std::string& pszFileName, DieFlags nFlags, std::string& pszDatabase)
{
    Check(0);
    const OriginalScanFileA_Sig OriginalFunction = reinterpret_cast<OriginalScanFileA_Sig>(__FunctionPointers[0]);
    auto res = OriginalFunction(pszFileName.data(), static_cast<int>(nFlags), pszDatabase.data());
    if ( res )
        return std::string(res);
    return std::nullopt;
}

std::optional<std::wstring>
ScanFileW(std::wstring& pwszFileName, DieFlags nFlags, std::wstring& pwszDatabase)
{
    Check(1);
    const OriginalScanFileW_Sig OriginalFunction = reinterpret_cast<OriginalScanFileW_Sig>(__FunctionPointers[1]);
    auto res = OriginalFunction(pwszFileName.data(), static_cast<int>(nFlags), pwszDatabase.data());
    if ( res )
        return std::wstring(res);
    return std::nullopt;
}

void
FreeMemoryA(std::string& pszString)
{
    Check(2);
    const OriginalFreeMemoryA_Sig OriginalFunction = reinterpret_cast<OriginalFreeMemoryA_Sig>(__FunctionPointers[2]);
    return OriginalFunction(pszString.data());
}

void
FreeMemoryW(std::string& pwszString)
{
    Check(3);
    const OriginalFreeMemoryW_Sig OriginalFunction = reinterpret_cast<OriginalFreeMemoryW_Sig>(__FunctionPointers[3]);
    return OriginalFunction(pwszString.data());
}

int
VB_ScanFile(wchar_t* pwszFileName, unsigned int nFlags, wchar_t* pwszDatabase, wchar_t* pwszBuffer, int nBufferSize)
{
    // return ::DIE_VB_ScanFile(pwszFileName, nFlags, pwszDatabase, pwszBuffer, nBufferSize);
    return -1;
}

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

    m.doc()               = "The native `die` module";
    m.attr("__version__") = "0.1.0";

    m.def("ScanFileA", DIE::ScanFileA);
    m.def("ScanFileW", DIE::ScanFileW);
    m.def("FreeMemoryA", DIE::FreeMemoryA);
    m.def("FreeMemoryW", DIE::FreeMemoryW);
}
