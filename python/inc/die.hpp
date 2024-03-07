#pragma once

#include <optional>
#include <string>

#include "die.h"

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
VB_ScanFile(wchar_t* pwszFileName, unsigned int nFlags, wchar_t* pwszDatabase, wchar_t* pwszBuffer, int nBufferSize);
} // namespace DIE