import pathlib


def test_basic_import():
    die = __import__("die")
    dbpath = die.database_path
    assert dbpath.exists()

    res = die.scan_file(
        pathlib.Path("c:/windows/system32/ntdll.dll"),
        die.ScanFlags.Deepscan,
        dbpath / "PE/UPX lock.2.sg",
    )
    assert res == "PE64"
