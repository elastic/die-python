import pathlib

# import os

# package_path = pathlib.Path(__path__[0])
# os.environ["LD_LIBRARY_PATH"] = (
#     os.environ.get("LD_LIBRARY_PATH", "") + ":" + str(package_path.absolute())
# )

from typing import Optional
from . import __package__
from ._die import __version__
from ._die import DieFlags as ScanFlags
from ._die import ScanFileA as _ScanFileA
from ._die import SetSitePackagePath as _SetSitePackagePath
from ._die import GetSitePackagePath as _GetSitePackagePath

_SetSitePackagePath(pathlib.Path(__path__[0]))

version_major, version_minor, version_patch = map(int, __version__.split("."))
database_path = _GetSitePackagePath() / "db"
"""Path to the DIE signature database"""


version_major, version_minor, version_patch = map(int, __version__.split("."))

database_path = pathlib.Path(__path__[0]) / "db"
"""Path to the DIE signature database"""


def scan_file(
    filepath: pathlib.Path, flags: ScanFlags, database: pathlib.Path | None
) -> Optional[str]:
    """Scan the given file against the signature database"""
    assert filepath.exists()
    if database:
        assert database.exists()
    db_str = str(database.absolute()) if database else None
    res = _ScanFileA(str(filepath.absolute()), flags, db_str)
    if not res:
        return None
    return res.strip()
