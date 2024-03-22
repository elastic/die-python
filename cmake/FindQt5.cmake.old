include( FetchContent )

set(QT5_VERSION_MAJOR 5)
set(QT5_VERSION_MINOR 15)
set(QT5_VERSION_PATCH 2)

FetchContent_Declare(
    Qt5
    URL https://download.qt.io/official_releases/qt/5.15/5.15.2/single/qt-everywhere-src-5.15.2.zip
    # URL http://localhost:8000/qt-everywhere-src-5.15.2.zip
    URL_HASH SHA1=d61cdf87f0b7705c05dc549778e96b2d872e711d
    CONFIGURE_COMMAND "perl init-repository"
)

set(QT_BUILD_SUBMODULES
    qtbase
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
    # qtscxml
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
set(QT_FEATURE_concurrent OFF)
set(QT_FEATURE_sql OFF)
set(QT_FEATURE_network OFF)
set(QT_FEATURE_xml OFF)
set(QT_FEATURE_dbus OFF)
set(QT_FEATURE_gui OFF)
set(QT_FEATURE_testlib OFF)
set(QT_FEATURE_printsupport OFF)

FetchContent_MakeAvailable( Qt5 )

message(STATUS "Using Qt5 in '${qt5_SOURCE_DIR}'")

set(CMAKE_AUTOUIC OFF)
set(CMAKE_AUTOMOC OFF)
set(CMAKE_AUTORCC OFF)

