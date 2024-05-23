# DetectItEasy-Python

[![python 3](https://img.shields.io/badge/python-3.8+-cyan)](https://python.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Licence MIT](https://img.shields.io/packagist/l/doctrine/orm.svg?maxAge=2592000?style=plastic)](https://github.com/hugsy/die-python/blob/main/LICENSE)

Python3 bindings for [@horsicq](https://github.com/horsicq/)'s [Detect-It-Easy](https://github.com/horsicq/Detect-It-Easy)


## Install

> [!NOTE]
> Building from source may be quite long and resource intensive as it requires to build Qt6.

### From PIP

> [!CAUTION]
> WIP - Not ready yet

```console
```

### From Github

```console
python -m pip install -e "git+https://github.com/calladoum-elastic/die-python.git/#egg=die-python"
```

### Using Git

```console
git clone https://github.com/calladoum-elastic/die-python
python -m pip install . --user -U
```

## Usage

```python
import die, pathlib

result = die.scan_file(
        pathlib.Path("c:/windows/system32/ntdll.dll"),
        die.ScanFlags.Deepscan,
        die.database_path / "PE/UPX lock.2.sg"
)
assert result is not None
```
