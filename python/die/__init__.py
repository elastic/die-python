import enum
from typing import Optional
from ._die import DIE_libdie as _DIE_libdie
from ._die import SF as _SF


class ScanFlags(enum.IntFlag):
    SF_DEEPSCAN = _SF.SF_DEEPSCAN
    SF_HEURISTICSCAN = _SF.SF_HEURISTICSCAN
    SF_ALLTYPESSCAN = _SF.SF_ALLTYPESSCAN
    SF_RECURSIVESCAN = _SF.SF_RECURSIVESCAN
    SF_VERBOSE = _SF.SF_VERBOSE
    SF_RESULTASXML = _SF.SF_RESULTASXML
    SF_RESULTASJSON = _SF.SF_RESULTASJSON
    SF_RESULTASTSV = _SF.SF_RESULTASTSV
    SF_RESULTASCSV = _SF.SF_RESULTASCSV


def scan_file(file: str, flags: ScanFlags, database: str) -> Optional[str]:
    """Scan the given file"""
    return _DIE_libdie().scanFile(file, flags, database)
