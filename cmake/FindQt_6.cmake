include( FetchContent )

set(QT6_VERSION_MAJOR 6)
set(QT6_VERSION_MINOR 7)
set(QT6_VERSION_PATCH 1)

set(QT_VERSION_MAJOR ${QT6_VERSION_MAJOR})
set(QT_VERSION_MINOR ${QT6_VERSION_MINOR})
set(QT_VERSION_PATCH ${QT6_VERSION_PATCH})

message(STATUS "Fetching Qt6 v${QT6_VERSION_MAJOR}.${QT6_VERSION_MINOR}.${QT6_VERSION_PATCH}")
FetchContent_Declare(
    Qt6
    # URL https://download.qt.io/official_releases/qt/${QT6_VERSION_MAJOR}.${QT6_VERSION_MINOR}/${QT6_VERSION_MAJOR}.${QT6_VERSION_MINOR}.${QT6_VERSION_PATCH}/single/qt-everywhere-src-${QT6_VERSION_MAJOR}.${QT6_VERSION_MINOR}.${QT6_VERSION_PATCH}.zip
    URL https://download.qt.io/official_releases/qt/6.7/6.7.1/single/qt-everywhere-src-6.7.1.zip
    URL_HASH SHA1=870cdbd688819bc45ce5eb3cf9833765da0bb85d
    # URL https://download.qt.io/official_releases/qt/6.6/6.6.2/single/qt-everywhere-src-6.6.2.zip
    # URL_HASH SHA1=e0f6a12c7c93ee9bda2597f63a763131f4727cd2
    # CONFIGURE_COMMAND "./configure"
)

set(QT_BUILD_SUBMODULES
    qtbase
    qtdeclarative
    qttools
    qtsvg
    # qtscxml
    # qt3d
    # qt5compat
    # qtactiveqt
    # qtcharts
    # qtcoap
    # qtconnectivity
    # qtdatavis3d
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
    # qttranslations
    # qtvirtualkeyboard
    # qtwayland
    # qtwebchannel
    # qtwebengine
    # qtwebsockets
    # qtwebview
)

# QtBase features
set(QT_FEATURE_core ON)
set(QT_FEATURE_xml ON)
set(QT_FEATURE_concurrent ON)
set(QT_FEATURE_qml ON)
set(QT_FEATURE_network ON)
set(QT_FEATURE_sql OFF)
set(QT_FEATURE_dbus OFF)
set(QT_FEATURE_gui OFF)
set(QT_FEATURE_testlib OFF)
set(QT_FEATURE_printsupport OFF)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

list(APPEND CMAKE_MODULE_PATH "${qt6_SOURCE_DIR}/cmake")
set(QT_DIR "C:/git/die-python/build/build-unknown/_deps/qt6-build/qtbase/lib/cmake/Qt6")

set(QT_SOURCE_DIR build/build-x64/_deps/qt6-src)
set(QT_SUBBUILD_DIR  ${qt6_SOURCE_DIR}/../qt6-subbuild)
set(QT_BUILD_DIR  ${qt6_SOURCE_DIR}/../qt6-build)

message(STATUS "Configuring Qt... (src=${QT_SOURCE_DIR}, dst=${QT_BUILD_DIR})" )

execute_process(
    COMMAND ${QT_SOURCE_DIR}/configure -prefix ${QT_SUBBUILD_DIR} -skip qtbluetooth -skip qtconnectivity
    COMMAND ${CMAKE_COMMAND} --build ${QT_SUBBUILD_DIR} --parallel
    COMMAND_ECHO STDOUT
    WORKING_DIRECTORY ${QT_SUBBUILD_DIR}
)

FetchContent_MakeAvailable(Qt6)

message(STATUS "Using Qt6 in '${qt6_SOURCE_DIR}'")

