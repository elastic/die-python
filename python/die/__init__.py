import enum
import pathlib
import warnings

from typing import Generator

from ._die import __version__  # ty:ignore[unresolved-import]
from ._die import DieFlags as _DieFlags  # ty:ignore[unresolved-import]
from ._die import (  # ty:ignore[unresolved-import]
    ScanFileA as _ScanFileA,
    ScanFileExA as _ScanFileExA,
    ScanMemoryA as _ScanMemoryA,
    ScanMemoryExA as _ScanMemoryExA,
    LoadDatabaseA as _LoadDatabaseA,
)
from ._die import die_version, dielib_version, dielib_tag  # ty:ignore[unresolved-import]

__all__ = ["die_version", "dielib_version", "dielib_tag"]
version_major, version_minor, version_patch = map(int, __version__.split("."))


# Use concrete Path type to maintain isinstance() compatibility
_BasePath = type(pathlib.Path())


class _DatabasePath(_BasePath):  # ty:ignore[unsupported-base]
    """
    Smart database path that maintains backward compatibility.

    This class automatically handles both old and new usage patterns:
    - New code: use database_path directly
    - Old code: database_path / 'db' still works but shows deprecation warning

    The path detection works as follows:
    1. If db/PE/ exists (new fixed version): use this path
    2. If db/db/PE/ exists (old buggy version): use the nested path
    """

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args)
        obj._resolved_path_str = None
        return obj

    def _get_resolved_str(self):
        """Resolve and return the actual database path as a string."""
        # Use getattr with default to handle Python 3.9's pathlib behavior
        # where __new__ may not be called in path operations
        # See: https://github.com/python/cpython/issues/100479
        resolved = getattr(self, "_resolved_path_str", None)

        if resolved is None:
            # Use parent class's __str__ to get path without triggering our override
            # This avoids recursion when __str__ calls _get_resolved_str
            path_str = super().__str__()
            concrete_path = pathlib.Path(path_str)

            if (concrete_path / "PE").exists():
                resolved = path_str
            elif (concrete_path / "db/PE").exists():
                resolved = str(concrete_path / "db")
            else:
                resolved = path_str

            self._resolved_path_str = resolved

        return resolved

    def __truediv__(self, other):
        """Handle path concatenation with backward compatibility."""
        if other == "db":
            # User is using the old workaround: database_path / 'db'
            # Check if the base path (before resolution) already contains PE/
            # If yes, this is the new version and /'db' is redundant
            base_path_str = super().__str__()
            base_path = pathlib.Path(base_path_str)

            if (base_path / "PE").exists():
                # New fixed version: database is at die/db/PE/
                warnings.warn(
                    "Using 'database_path / \"db\"' is deprecated and no longer needed. "
                    "The database is now directly at 'database_path'. "
                    "Simply use 'database_path' instead.",
                    DeprecationWarning,
                    stacklevel=2,
                )
                return self
            # else: Old version, database is at die/db/db/PE/
            # The /'db' is necessary, allow it to proceed

        # Default behavior: use parent's __truediv__ for normal path concatenation
        return super().__truediv__(other)

    def __str__(self):
        """Return the resolved database path as a string."""
        return self._get_resolved_str()

    def __fspath__(self):
        """Return the resolved database path for os.fspath()."""
        return self._get_resolved_str()

    def exists(self):
        """Check if the resolved database path exists."""
        return pathlib.Path(self._get_resolved_str()).exists()

    def iterdir(self):
        """Iterate over the resolved database path."""
        return pathlib.Path(self._get_resolved_str()).iterdir()


# Initialize database path with smart handling
database_path = _DatabasePath(__path__[0]) / "db"
"""Path to the DIE signature database

This path automatically points to the correct database location,
regardless of how the package is laid out:
- When the database directory is installed directly at die/db/
- When the database directory is installed at die/db/db/

Usage:
    # Recommended:
    die.scan_file(file, flags, str(die.database_path))

    # Legacy code (still works, but may show a deprecation warning):
    die.scan_file(file, flags, str(die.database_path / 'db'))
"""


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
    filepath: pathlib.Path | str, flags: ScanFlags, database: str | None = None
) -> str | None:
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
    memory: bytes | bytearray, flags: ScanFlags, database: str | None = None
) -> str | None:
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


def load_database(database: str | pathlib.Path) -> int:
    """
    Load a database
    """
    if isinstance(database, pathlib.Path):
        database = str(database)

    elif not isinstance(database, str):
        raise TypeError

    return _LoadDatabaseA(database)
