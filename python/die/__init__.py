import pathlib
import platform
from typing import Optional
from . import __package__
from ._die import __version__
from ._die import DieFlags as ScanFlags
from ._die import ScanFileA as _ScanFileA
from ._die import SetSitePackagePath as _SetSitePackagePath
from ._die import GetSitePackagePath as _GetSitePackagePath

assert platform.system() == "Windows", f"die-python currently only works on Windows"

_SetSitePackagePath(pathlib.Path(__path__[0]))

version_major, version_minor, version_patch = map(int, __version__.split("."))
database_path = _GetSitePackagePath() / "db"
"""Path to the DIE signature database"""


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
