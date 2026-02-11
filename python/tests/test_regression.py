import json
import pathlib

import die

TESTS_FOLDER = pathlib.Path(__file__).parent.absolute()
DATA_FOLDER = TESTS_FOLDER / "data"
DB_FOLDER = die.database_path


def test_issue_28():
    # issue https://github.com/elastic/die-python/issues/28
    # pr https://github.com/elastic/die-python/pull/30
    fpath = DATA_FOLDER / "test.rar"
    res = die.scan_file(fpath, die.ScanFlags.RESULT_AS_JSON, str(DB_FOLDER))
    assert res
    js = json.loads(res)
    assert len(js["detects"]) == 1
    assert js["detects"][0]["filetype"] == "Binary"

    values = js["detects"][0]["values"]
    assert len(values) > 0
    value = values[0]
    assert value["name"] == "RAR"
    assert value["string"].startswith("Archive: RAR(")
