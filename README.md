# DetectItEasy-Python

[![Python 3.8+](https://img.shields.io/pypi/v/die-python.svg)](https://pypi.org/project/die-python/)
[![Downloads](https://static.pepy.tech/badge/die-python)](https://pepy.tech/project/die-python)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Licence Apache2](https://img.shields.io/badge/License-Apache_2-blue)](https://github.com/elastic/die-python/blob/main/LICENSE)
[![Build](https://github.com/elastic/die-python/actions/workflows/build.yml/badge.svg)](https://github.com/elastic/die-python/actions/workflows/build.yml)

Native Python 3.8+ bindings for [@horsicq](https://github.com/horsicq/)'s [Detect-It-Easy](https://github.com/horsicq/Detect-It-Easy)


## Install

### From PIP

The easiest and recommended installation is through `pip`.

```console
pip install die-python
```

### Using Git

```console
git clone https://github.com/elastic/die-python
cd die-python
```

Install Qt into the `build`. It can be easily installed using [`aqt`](https://github.com/miurahr/aqtinstall) as follow (here with Qt version 6.7.3):

```console
python -m pip install aqtinstall --user -U
python -m aqt install-qt -O ./build linux desktop 6.7.3 linux_gcc_64               # linux x64 only
python -m aqt install-qt -O ./build linux_arm64 desktop 6.7.3 linux_gcc_arm64      # linux arm64 only
python -m aqt install-qt -O ./build windows desktop 6.7.3 win64_msvc2019_64        # windows x64 only
python -m aqt install-qt -O ./build mac desktop 6.7.3 clang_64                     # mac only
```

Then you can install the package

```console
python -m pip install . --user -U
```


## Quick start

```python
import die, pathlib

print(die.scan_file("c:/windows/system32/ntdll.dll", die.ScanFlags.DEEP_SCAN))
'PE64'

print(die.scan_file("../upx.exe", die.ScanFlags.RESULT_AS_JSON, str(die.database_path) ))
{
    "detects": [
        {
            "filetype": "PE64",
            "parentfilepart": "Header",
            "values": [
                {
                    "info": "Console64,console",
                    "name": "GNU linker ld (GNU Binutils)",
                    "string": "Linker: GNU linker ld (GNU Binutils)(2.28)[Console64,console]",
                    "type": "Linker",
                    "version": "2.28"
                },
                {
                    "info": "",
                    "name": "MinGW",
                    "string": "Compiler: MinGW",
                    "type": "Compiler",
                    "version": ""
                },
                {
                    "info": "NRV,brute",
                    "name": "UPX",
                    "string": "Packer: UPX(4.24)[NRV,brute]",
                    "type": "Packer",
                    "version": "4.24"
                }
            ]
        }
    ]
}

for db in die.databases():
    print(db)
\path\to\your\pyenv\site-packages\die\db\ACE
\path\to\your\pyenv\site-packages\die\db\Amiga\DeliTracker.1.sg
\path\to\your\pyenv\site-packages\die\db\Amiga\_Amiga.0.sg
\path\to\your\pyenv\site-packages\die\db\Amiga\_init
\path\to\your\pyenv\site-packages\die\db\APK\AlibabaProtection.2.sg
[...]
```

## Licenses

Released under Apache 2.0 License and integrates the following repositories:

 - [Detect-It-Easy](https://github.com/horsicq/Detect-It-Easy): MIT license
 - [die_library](https://github.com/horsicq/die_library): MIT license
 - [qt](https://github.com/qt/qt): LGPL license
