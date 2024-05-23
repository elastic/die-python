#include <stdint.h>

#include <optional>
#include <string>

#include "die.h"

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
ScanFileA(std::string& pszFileName, DieFlags nFlags, std::string& pszDatabase);

std::optional<std::wstring>
ScanFileW(std::wstring& pwszFileName, DieFlags nFlags, std::wstring& pwszDatabase);

void
FreeMemoryA(std::string& pszString);

void
FreeMemoryW(std::wstring& pwszString);

#ifdef _WIN32
int
VB_ScanFile(
    std::wstring& pwszFileName,
    DieFlags nFlags,
    std::wstring& pwszDatabase,
    std::wstring& pwszBuffer,
    size_t nBufferSize);
#endif // _WIN32

} // namespace DIE

#endif
