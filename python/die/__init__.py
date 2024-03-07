import pathlib
from typing import Optional
from ._die import DieFlags as ScanFlags
from ._die import ScanFileA as _ScanFileA
from ._die import __version__
from . import __package__

version_major, version_minor, version_patch = map(int, __version__.split("."))

database_path = pathlib.Path(__path__[0]) / "db"


def scan_file(
    filepath: pathlib.Path, flags: ScanFlags, database: pathlib.Path
) -> Optional[str]:
    """Scan the given file against the signature database"""
    assert filepath.exists()
    assert database.exists()
    res = _ScanFileA(str(filepath.absolute()), flags, str(database.absolute()))
    if not res:
        return None
    return res.strip()
