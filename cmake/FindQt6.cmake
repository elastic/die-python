include( FetchContent )

set(QT6_VERSION_MAJOR 6)
set(QT6_VERSION_MINOR 6)
set(QT6_VERSION_PATCH 2)

FetchContent_Declare(
    Qt6
    # GIT_REPOSITORY "https://github.com/qt/qt5"
    # GIT_TAG v6.6.2
    URL https://download.qt.io/official_releases/qt/6.6/6.6.2/single/qt-everywhere-src-6.6.2.zip
    URL_HASH SHA1=e0f6a12c7c93ee9bda2597f63a763131f4727cd2
    # CONFIGURE_COMMAND "perl init-repository"
)

FetchContent_MakeAvailable( Qt6 )

message(STATUS "Using Qt6 in '${qt6_SOURCE_DIR}'")

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
