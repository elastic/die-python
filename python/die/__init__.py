import pathlib

from typing import Optional
from ._die import __version__
from ._die import DieFlags as ScanFlags
from ._die import ScanFileA as _ScanFileA

version_major, version_minor, version_patch = map(int, __version__.split("."))

database_path = pathlib.Path(__path__[0]) / "db"
"""Path to the DIE signature database"""


def scan_file(
    filepath: pathlib.Path | str, flags: ScanFlags, database: str = ""
) -> Optional[str]:
    """
    Scan the given file against the signature database

    Arguments:
        filepath: pathlib.Path | str
        flags: ScanFlags
        database: str = ""

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
    if not isinstance(database, str):
        raise TypeError
    else:
        _db = database

    res = _ScanFileA(str(_fpath), flags, _db)
    if not res:
        return None
    return res.strip()
