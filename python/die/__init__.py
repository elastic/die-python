import enum
import pathlib

from typing import Generator, Optional, Union

from ._die import __version__  # type: ignore
from ._die import DieFlags as _DieFlags  # type: ignore
from ._die import (
    ScanFileA as _ScanFileA,  # type: ignore
    ScanFileExA as _ScanFileExA,  # type: ignore
    ScanMemoryA as _ScanMemoryA,  # type: ignore
    ScanMemoryExA as _ScanMemoryExA,  # type: ignore
    LoadDatabaseA as _LoadDatabaseA,  # type: ignore
)
from ._die import die_version, dielib_version  # type: ignore

version_major, version_minor, version_patch = map(int, __version__.split("."))

database_path = pathlib.Path(__path__[0]) / "db"
"""Path to the DIE signature database"""


class ScanFlags(enum.IntFlag):
    ALL_TYPES_SCAN = _DieFlags.AlltypesScan.value
    DEEP_SCAN = _DieFlags.Deepscan.value
    HEURISTIC_SCAN = _DieFlags.HeuristicScan.value
    RECURSIVE_SCAN = _DieFlags.RecursiveScan.value
    RESULT_AS_CSV = _DieFlags.ResultAsCsv.value
    RESULT_AS_JSON = _DieFlags.ResultAsJson.value
    RESULT_AS_TSV = _DieFlags.ResultAsTsv.value
    RESULT_AS_XML = _DieFlags.ResultAsXml.value
    VERBOSE_FLAG = _DieFlags.Verbose.value


def scan_file(
    filepath: Union[pathlib.Path, str], flags: ScanFlags, database: Optional[str] = None
) -> Optional[str]:
    """
    Scan the given file against the signature database, if specified

    Arguments:
        filepath: Union[pathlib.Path, str]
        flags: ScanFlags
        database: Optional[str]

    Returns:
        Optional[str]
    """
    # Check `filepath`
    if isinstance(filepath, str):
        _fpath = pathlib.Path(filepath)
    elif isinstance(filepath, pathlib.Path):
        _fpath = filepath
    else:
        raise TypeError
    assert _fpath.exists()

    # Check `database`
    if database is None:
        res = _ScanFileExA(str(_fpath), flags)
    elif isinstance(database, str):
        res = _ScanFileA(str(_fpath), flags, database)
    else:
        raise TypeError

    if not res:
        return None
    return res.strip()


def databases() -> Generator[pathlib.Path, None, None]:
    """
    Enumerate all databases

    Returns:
        Generator[pathlib.Path, None, None]
    """

    def __enum_db(root: pathlib.Path) -> Generator[pathlib.Path, None, None]:
        for child in root.iterdir():
            if child.is_file():
                yield child
            if child.is_dir():
                yield from __enum_db(child)

    return __enum_db(database_path)


def scan_memory(
    memory: Union[bytes, bytearray], flags: ScanFlags, database: Optional[str] = None
) -> Optional[str]:
    """
    Scan the given sequence of bytes against the signature database, if specified

    Arguments:
        memory: bytes
        flags: ScanFlags
        database: Optional[str]

    Returns:
        Optional[str]
    """
    if not isinstance(memory, bytes) and not isinstance(memory, bytearray):
        raise TypeError

    if database is None:
        res = _ScanMemoryExA(memory, flags)
    elif isinstance(database, str):
        res = _ScanMemoryA(memory, flags, database)
    else:
        raise TypeError

    if not res:
        return None
    return res.strip()


def load_database(database: str) -> int:
    """
    Load a database
    """
    if not isinstance(database, str):
        raise TypeError

    return _LoadDatabaseA(database)
