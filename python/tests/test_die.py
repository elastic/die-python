import pathlib
import platform

import die

default_target = (
    pathlib.Path("c:/windows/system32/winver.exe")
    if platform.system() == "Windows"
    else pathlib.Path("/bin/ls")
)


def test_basic_import():
    dbpath: pathlib.Path = die.database_path
    assert dbpath.exists()

    res = die.scan_file(
        default_target,
        die.ScanFlags.Deepscan,
    )

    if platform.system() == "Windows":
        assert res == "PE64"
    elif platform.system() == "Linux":
        assert res == "ELF64"
