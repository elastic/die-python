#ifndef DIELIB_H
#define DIELIB_H


#ifdef _WIN32
#include <windows.h>
#else
#include <dlfcn.h>
#endif // _WIN32

#ifdef __cplusplus
#include <optional>
#include <string>
#endif // __cplusplus

#include <stdint.h>

// flags
#define DIE_DEEPSCAN 0x00000001
#define DIE_HEURISTICSCAN 0x00000002
#define DIE_ALLTYPESSCAN 0x00000004
#define DIE_RECURSIVESCAN 0x00000008
#define DIE_VERBOSE 0x00000010
#define DIE_RESULTASXML 0x00010000
#define DIE_RESULTASJSON 0x00020000
#define DIE_RESULTASTSV 0x00040000
#define DIE_RESULTASCSV 0x00080000

#ifdef __cplusplus
extern "C"
{
#endif

    char*
    DIE_ScanFileA(char* pszFileName, unsigned int nFlags, char* pszDatabase);
    wchar_t*
    DIE_ScanFileW(wchar_t* pwszFileName, unsigned int nFlags, wchar_t* pwszDatabase);
    void
    DIE_FreeMemoryA(char* pszString);
    void
    DIE_FreeMemoryW(char* pwszString);
    int
    DIE_VB_ScanFile(
        wchar_t* pwszFileName,
        unsigned int nFlags,
        wchar_t* pwszDatabase,
        wchar_t* pwszBuffer,
        int nBufferSize);

#ifdef _WIN32
#ifdef UNICODE
#define DIE_ScanFile DIE_ScanFileW
#define DIE_FreeMemory DIE_FreeMemoryW
#else
#define DIE_ScanFile DIE_ScanFileA
#define DIE_FreeMemory DIE_FreeMemoryA
#endif
#endif // _WIN32

#ifdef __cplusplus
}

namespace DIE
{
enum class DieFlags : uint32_t
{
    Deepscan      = DIE_DEEPSCAN,
    HeuristicScan = DIE_HEURISTICSCAN,
    AlltypesScan  = DIE_ALLTYPESSCAN,
    RecursiveScan = DIE_RECURSIVESCAN,
    Verbose       = DIE_VERBOSE,
    ResultAsXml   = DIE_RESULTASXML,
    ResultAsJson  = DIE_RESULTASJSON,
    ResultAsTsv   = DIE_RESULTASTSV,
    ResultAsCsv   = DIE_RESULTASCSV,
};

std::optional<std::string>
ScanFileA(std::string& pszFileName, DieFlags nFlags, std::string& pszDatabase);

std::optional<std::wstring>
ScanFileW(std::wstring& pwszFileName, DieFlags nFlags, std::wstring& pwszDatabase);

void
FreeMemoryA(std::string& pszString);

void
FreeMemoryW(std::string& pwszString);

int
VB_ScanFile(
    std::wstring& pwszFileName,
    DieFlags nFlags,
    std::wstring& pwszDatabase,
    std::wstring& pwszBuffer,
    size_t nBufferSize);

} // namespace DIE

#endif

#endif // DIELIB_H