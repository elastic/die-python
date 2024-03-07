import pathlib


def test_basic_import():
    die = __import__("die")
    pkgpath = pathlib.Path(die.__path__[0])
    assert pkgpath.exists()
    dbpath = pkgpath / "db"
    assert dbpath.exists()

    res = die.scan_file(
        pathlib.Path("c:/windows/system32/ntdll.dll"),
        die._die.DieFlags.Deepscan,
        dbpath / "PE/UPX lock.2.sg",
    )
    assert res == "PE64"
