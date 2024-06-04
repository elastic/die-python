import pathlib
import platform
import json

import bs4

import die


def test_constants():
    # version
    assert isinstance(die.version_major, int)
    assert isinstance(die.version_minor, int)
    assert isinstance(die.version_patch, int)

    # validate die database
    assert isinstance(die.database_path, pathlib.Path)
    assert die.database_path.exists()
    assert die.database_path.is_dir()

    # validate scan flags
    assert die._DieFlags.Deepscan.value == die.ScanFlags.DEEP_SCAN
    assert die._DieFlags.HeuristicScan.value == die.ScanFlags.HEURISTIC_SCAN
    assert die._DieFlags.AlltypesScan.value == die.ScanFlags.ALL_TYPES_SCAN
    assert die._DieFlags.RecursiveScan.value == die.ScanFlags.RECURSIVE_SCAN
    assert die._DieFlags.Verbose.value == die.ScanFlags.VERBOSE_FLAG
    assert die._DieFlags.ResultAsXml.value == die.ScanFlags.RESULT_AS_XML
    assert die._DieFlags.ResultAsJson.value == die.ScanFlags.RESULT_AS_JSON
    assert die._DieFlags.ResultAsTsv.value == die.ScanFlags.RESULT_AS_TSV
    assert die._DieFlags.ResultAsCsv.value == die.ScanFlags.RESULT_AS_CSV
    # validate no new flag was added and not test
    assert sorted([x for x in dir(die._DieFlags) if not x.startswith("__")]) == sorted(
        [
            "AlltypesScan",
            "Deepscan",
            "HeuristicScan",
            "RecursiveScan",
            "ResultAsCsv",
            "ResultAsJson",
            "ResultAsTsv",
            "ResultAsXml",
            "Verbose",
        ]
    )


def test_scan_basic():
    default_target = (
        pathlib.Path("c:/windows/system32/winver.exe")
        if platform.system() == "Windows"
        else pathlib.Path("/bin/ls")
    )

    res = die.scan_file(
        default_target,
        die.ScanFlags.DEEP_SCAN,
    )
    assert res

    if platform.system() == "Windows":
        assert res == "PE64"
    elif platform.system() == "Linux":
        assert res == "ELF64"


def test_scan_export_format():
    default_target = (
        pathlib.Path("c:/windows/system32/winver.exe")
        if platform.system() == "Windows"
        else pathlib.Path("/bin/ls")
    )

    # JS
    res = die.scan_file(
        default_target,
        die.ScanFlags.DEEP_SCAN | die.ScanFlags.RESULT_AS_JSON,
    )
    assert res

    js = json.loads(res)
    assert len(js["detects"])
    if platform.system() == "Windows":
        assert js["detects"][0]["string"] == "PE64"
    elif platform.system() == "Linux":
        assert js["detects"][0]["string"] == "ELF64"

    # XML
    res = die.scan_file(
        default_target,
        die.ScanFlags.DEEP_SCAN | die.ScanFlags.RESULT_AS_XML,
    )
    assert res
    xml = bs4.BeautifulSoup(res, "xml")
    assert xml.Result
    if platform.system() == "Windows":
        assert xml.Result.detect.text == "PE64"
    elif platform.system() == "Linux":
        assert xml.Result.detect.text == "ELF64"

    # CSV
    res = die.scan_file(
        default_target,
        die.ScanFlags.DEEP_SCAN | die.ScanFlags.RESULT_AS_CSV,
    )
    assert res

    assert len(res.splitlines()) == 1
    parts = res.split(";")
    assert len(parts) == 5
    if platform.system() == "Windows":
        assert parts[-1] == "PE64"
    elif platform.system() == "Linux":
        assert parts[-1] == "ELF64"


def test_basic_databases():
    for db in die.databases():
        assert isinstance(db, pathlib.Path)
        assert db.exists()
        assert db.is_file()
