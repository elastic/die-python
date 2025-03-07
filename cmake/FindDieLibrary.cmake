include(FetchContent)

set(ROOT_DIR "${CMAKE_CURRENT_LIST_DIR}/..")

# Only use Qt6

set(QT_BUILD_VERSION "6.6.2")

if(WIN32)
  # python -m aqt install-qt -O build windows desktop ${QT_BUILD_VERSION} win64_msvc2019_64
  set(QT_BUILD_COMPILER "msvc2019_64")
elseif(LINUX)
  # python -m aqt install-qt -O build linux desktop ${QT_BUILD_VERSION} gcc_64
  set(QT_BUILD_COMPILER "gcc_64")
elseif(APPLE)
  # python -m aqt install-qt -O build mac desktop ${QT_BUILD_VERSION} clang_64
  set(QT_BUILD_COMPILER "macos")
else()
  message(FATAL "nope")
endif()

set(Qt6_DIR "${ROOT_DIR}/build/${QT_BUILD_VERSION}/${QT_BUILD_COMPILER}/lib/cmake/Qt6")
set(QT_DIR ${Qt6_DIR})
list(APPEND CMAKE_MODULE_PATH ${Qt6_DIR})

find_package(Qt6 REQUIRED COMPONENTS Core Qml Concurrent)

FetchContent_Declare(
  DieLibrary
  GIT_REPOSITORY "https://github.com/horsicq/die_library"
  GIT_TAG ef5542fec4467fb53a4fec60180f55e83c0c9c8f
)

set(DIE_BUILD_AS_STATIC ON CACHE INTERNAL "")
FetchContent_MakeAvailable( DieLibrary )

message(STATUS "Using DieLibrary in '${dielibrary_SOURCE_DIR}'")

list(APPEND CMAKE_MODULE_PATH "${dielibrary_SOURCE_DIR}/dep/build_tools/cmake")
