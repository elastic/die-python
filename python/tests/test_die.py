import bs4
import json
import pathlib
import platform
import pytest

import die


def test_constants():
    # version
    assert isinstance(die.version_major, int)
    assert isinstance(die.version_minor, int)
    assert isinstance(die.version_patch, int)

    assert isinstance(die.die_version, str)
    assert die.die_version
    assert isinstance(die.dielib_version, str)
    assert die.dielib_version

    # validate die database
    assert isinstance(die.database_path, die._DatabasePath)
    assert die.database_path.exists()

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


@pytest.fixture
def target_binary():
    return (
        pathlib.Path("c:/windows/system32/winver.exe")
        if platform.system() == "Windows"
        else pathlib.Path("/bin/ls")
    )


def test_scan_memory(target_binary: pathlib.Path):
    raw_data = target_binary.read_bytes()
    res = die.scan_memory(
        bytearray(raw_data),
        die.ScanFlags.DEEP_SCAN,
    )
    assert res
    assert isinstance(res, str)

    lines = res.splitlines()
    assert len(lines)

    if platform.system() == "Windows":
        assert lines[0] == "PE64"
    elif platform.system() == "Linux":
        assert lines[0] == "ELF64"


def test_scan_basic(target_binary: pathlib.Path):
    res = die.scan_file(
        target_binary,
        die.ScanFlags.DEEP_SCAN,
    )
    assert res
    assert isinstance(res, str)

    lines = res.splitlines()
    assert len(lines)

    if platform.system() == "Windows":
        assert lines[0] == "PE64"
    elif platform.system() == "Linux":
        assert lines[0] == "ELF64"


def test_scan_export_format_json(target_binary: pathlib.Path):
    res = die.scan_file(
        target_binary,
        die.ScanFlags.DEEP_SCAN | die.ScanFlags.RESULT_AS_JSON,
    )
    assert res

    js = json.loads(res)
    assert len(js["detects"])
    if platform.system() == "Windows":
        assert js["detects"][0]["filetype"] == "PE64"
    elif platform.system() == "Linux":
        assert js["detects"][0]["filetype"] == "ELF64"


def test_scan_export_format_xml(target_binary: pathlib.Path) -> None:
    res = die.scan_file(
        target_binary,
        die.ScanFlags.DEEP_SCAN | die.ScanFlags.RESULT_AS_XML,
    )
    assert res
    xml = bs4.BeautifulSoup(res, "xml")
    assert xml.Result
    if platform.system() == "Windows":
        assert hasattr(xml.Result, "PE64")
        assert xml.Result.PE64["filetype"] == "PE64"
    elif platform.system() == "Linux":
        assert hasattr(xml.Result, "ELF64")
        assert xml.Result.ELF64["filetype"] == "ELF64"


def test_scan_export_format_csv(target_binary: pathlib.Path):
    CSV_DELIMITER = ";"
    res = die.scan_file(
        target_binary,
        die.ScanFlags.DEEP_SCAN | die.ScanFlags.RESULT_AS_CSV,
    )
    assert res
    assert len(res.splitlines()) == 1
    assert len(res.split(CSV_DELIMITER)) == 5


def test_scan_export_format_tsv(target_binary: pathlib.Path):
    res = die.scan_file(
        target_binary,
        die.ScanFlags.DEEP_SCAN | die.ScanFlags.RESULT_AS_TSV,
    )
    assert res

    lines = res.splitlines()
    assert len(lines)

    if platform.system() == "Windows":
        assert lines[0] == "PE64"
    elif platform.system() == "Linux":
        assert lines[0] == "ELF64"


def test_basic_databases():
    for db in die.databases():
        assert isinstance(db, pathlib.Path)
        assert db.exists()
        assert db.is_file()


def test_database_path_backward_compatibility():
    """Test backward compatibility for database_path usage."""
    import warnings

    # Test 1: New usage should work without warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        path_new = str(die.database_path)
        assert len(w) == 0, "New usage should not produce warnings"

    # Test 2: database_path should resolve to a valid location with PE/ directory
    db_path = pathlib.Path(path_new)
    assert db_path.exists(), f"Database path does not exist: {db_path}"
    assert (db_path / 'PE').exists(), f"PE directory not found at {db_path}"

    # Test 3: Old usage with /'db' should work through smart path resolution
    # The smart path should detect the version and handle accordingly
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        path_old = str(die.database_path / 'db')

        # The path should exist in both old and new versions
        assert pathlib.Path(path_old).exists(), f"Old usage path doesn't exist: {path_old}"

        # Check if this is the new fixed version (database at die/db/PE/)
        # by checking if base path contains PE/
        base_path = pathlib.Path(str(die.database_path).replace('\\db\\db', '\\db\\'))
        # Note: We can't easily check base_path, so we use warning presence

        if len(w) > 0:
            # New fixed version: got deprecation warning
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "database_path" in str(w[0].message).lower()
            # In new version, both should resolve to same location
            assert pathlib.Path(path_new) == pathlib.Path(path_old)
        else:
            # Old buggy version: no warning, /'db' is necessary
            # In old version, path_old should be die/db/db and path_new should also be die/db/db
            assert path_new == path_old


def test_database_path_resolves_correctly():
    """Test that database_path resolves to the actual database location."""
    # The resolved path should contain PE/ directory
    db_path = pathlib.Path(str(die.database_path))

    # Check for PE directory (main signature database)
    assert (db_path / 'PE').exists(), f"PE directory not found at {db_path}"

    # Check for other expected directories
    expected_dirs = ['PE', 'ELF', 'MACH']
    for dir_name in expected_dirs:
        assert (db_path / dir_name).exists() or (db_path / dir_name).exists(), \
            f"Expected directory {dir_name} not found at {db_path}"


def test_scan_with_explicit_database_path(target_binary: pathlib.Path):
    """Test that scan_file works with explicit database path."""
    import warnings

    # Test with new usage (no /'db')
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        res = die.scan_file(
            target_binary,
            die.ScanFlags.DEEP_SCAN,
            database=str(die.database_path)
        )
        assert res
        assert isinstance(res, str)

    # Test with old usage (with /'db')
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        res = die.scan_file(
            target_binary,
            die.ScanFlags.DEEP_SCAN,
            database=str(die.database_path / 'db')
        )
        assert res
        assert isinstance(res, str)
