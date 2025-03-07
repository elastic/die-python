import json
import pathlib

import die

TESTS_FOLDER = pathlib.Path(__file__).parent.absolute()
DATA_FOLDER = TESTS_FOLDER / "data"


def test_issue_48():
    # issue https://github.com/elastic/die-python/issues/28
    # pr https://github.com/elastic/die-python/pull/30
    fpath = DATA_FOLDER / "test.rar"
    res = die.scan_file(fpath, die.ScanFlags.RESULT_AS_JSON)
    assert res
    js = json.loads(res)
    assert len(js["detects"]) == 1
    assert js["detects"][0]["filetype"] != "Binary"  # would fail in 0.2.0
    assert js["detects"][0]["filetype"] == "Archive: RAR"
