#include <stdint.h>

#include <optional>
#include <string>
#include <vector>

#include "die.h"

#ifndef DIELIB_VERSION
#define DIELIB_VERSION ""
#endif // DIELIB_VERSION

#ifndef DIE_VERSION
#define DIE_VERSION ""
#endif // DIE_VERSION

#ifdef __cplusplus
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
ScanFileA(std::string& pszFileName, uint32_t nFlags, std::string& pszDatabase);

std::optional<std::string>
ScanFileExA(std::string& pszFileName, uint32_t nFlags);

std::optional<std::string>
ScanMemoryA(std::vector<uint8_t>& memory, uint32_t nFlags, std::string& pszDatabase);

std::optional<std::string>
ScanMemoryExA(std::vector<uint8_t>& pszFileName, uint32_t nFlags);

int32_t
LoadDatabaseA(std::string& pszDatabase);


#ifdef _WIN32
int
VB_ScanFile(
    std::wstring& pwszFileName,
    uint32_t nFlags,
    std::wstring& pwszDatabase,
    std::wstring& pwszBuffer,
    size_t nBufferSize);
#endif // _WIN32

} // namespace DIE

#endif
