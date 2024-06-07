# DetectItEasy-Python

Native Python 3.8+ bindings for [@horsicq](https://github.com/horsicq/)'s [Detect-It-Easy](https://github.com/horsicq/Detect-It-Easy)


## Install

### From PIP

> [!CAUTION]
> WIP - Not ready yet

```console
```



### Using Git

```console
git clone https://github.com/calladoum-elastic/die-python
cd die-python
```

Install Qt into the `build`. It can be easily installed using [`aqt`](https://github.com/miurahr/aqtinstall) as follow (here with Qt version 6.6.2):

```console
python -m pip install aqtinstall --user -U
python -m aqt install-qt -O ./build linux    desktop 6.6.2 gcc_64             # linux only
python -m aqt install-qt -O ./build windows  desktop 6.6.2 win64_msvc2019_64  # windows only
python -m aqt install-qt -O ./build mac      desktop 6.6.2 clang_64           # mac only
```

Then you can install the package

```console
python -m pip install . --user -U
```


## Quick start

```python
import die, pathlib

print(die.scan_file("c:/windows/system32/ntdll.dll", die.ScanFlags.Deepscan))
'PE64'

print(die.scan_file("../upx.exe", die.ScanFlags.RESULT_AS_JSON, str(die.database_path/'db') ))
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
C:\Users\User\AppData\Roaming\Python\Python312\site-packages\die\db\db\ACE
C:\Users\User\AppData\Roaming\Python\Python312\site-packages\die\db\db\APK\PackageName.1.sg
C:\Users\User\AppData\Roaming\Python\Python312\site-packages\die\db\db\APK\SingleJar.3.sg
C:\Users\User\AppData\Roaming\Python\Python312\site-packages\die\db\db\APK\_APK.0.sg
C:\Users\User\AppData\Roaming\Python\Python312\site-packages\die\db\db\APK\_init
C:\Users\User\AppData\Roaming\Python\Python312\site-packages\die\db\db\Archive\_init
C:\Users\User\AppData\Roaming\Python\Python312\site-packages\die\db\db\archive-file
C:\Users\User\AppData\Roaming\Python\Python312\site-packages\die\db\db\arj
C:\Users\User\AppData\Roaming\Python\Python312\site-packages\die\db\db\Binary\Amiga loadable.1.sg
C:\Users\User\AppData\Roaming\Python\Python312\site-packages\die\db\db\Binary\archive.7z.1.sg
[...]
```

## Licenses

Released under Apache 2.0 License and integrates the following repositories:

 - [Detect-It-Easy](https://github.com/horsicq/Detect-It-Easy): MIT license
 - [die_library](https://github.com/horsicq/die_library): MIT license
 - [qt](https://github.com/qt/qt): LGPL license
