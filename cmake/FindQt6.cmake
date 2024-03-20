include( FetchContent )

set(QT6_VERSION_MAJOR 6)
set(QT6_VERSION_MINOR 6)
set(QT6_VERSION_PATCH 2)

set(QT_VERSION_MAJOR ${QT6_VERSION_MAJOR})
set(QT_VERSION_MINOR ${QT6_VERSION_MINOR})
set(QT_VERSION_PATCH ${QT6_VERSION_PATCH})

FetchContent_Declare(
    Qt6
    URL https://download.qt.io/official_releases/qt/6.6/6.6.2/single/qt-everywhere-src-6.6.2.zip
    # URL http://localhost:8000/qt-everywhere-src-6.6.2.zip
    URL_HASH SHA1=e0f6a12c7c93ee9bda2597f63a763131f4727cd2
    CONFIGURE_COMMAND "./configure.bat"
)

set(QT_BUILD_SUBMODULES
    qtbase
    qtscxml
    # qt3d
    # qt5compat
    # qtactiveqt
    # qtcharts
    # qtcoap
    # qtconnectivity
    # qtdatavis3d
    # qtdeclarative
    # qtdoc
    # qtgraphs
    # qtgrpc
    # qthttpserver
    # qtimageformats
    # qtlanguageserver
    # qtlocation
    # qtlottie
    # qtmqtt
    # qtmultimedia
    # qtnetworkauth
    # qtopcua
    # qtpositioning
    # qtquick3d
    # qtquick3dphysics
    # qtquickeffectmaker
    # qtquicktimeline
    # qtremoteobjects
    # qtsensors
    # qtserialbus
    # qtserialport
    # qtshadertools
    # qtspeech
    # qtsvg
    # qttools
    # qttranslations
    # qtvirtualkeyboard
    # qtwayland
    # qtwebchannel
    # qtwebengine
    # qtwebsockets
    # qtwebview
)

# QtBase features
set(QT_FEATURE_xml ON)
set(QT_FEATURE_concurrent OFF)
set(QT_FEATURE_sql OFF)
set(QT_FEATURE_network OFF)
set(QT_FEATURE_dbus OFF)
set(QT_FEATURE_gui OFF)
set(QT_FEATURE_testlib OFF)
set(QT_FEATURE_printsupport OFF)

set(CMAKE_AUTOUIC OFF)
set(CMAKE_AUTOMOC OFF)
set(CMAKE_AUTORCC OFF)

list(APPEND CMAKE_MODULE_PATH "${qt6_SOURCE_DIR}/cmake")
FetchContent_MakeAvailable(Qt6)

message(STATUS "Using Qt6 in '${qt6_SOURCE_DIR}'")
