include(FetchContent)

set(ROOT_DIR "${CMAKE_CURRENT_LIST_DIR}/..")

# Only use Qt6

set(QT_BUILD_VERSION "6.8.2")

if(WIN32)
  # python -m aqt install-qt -O build windows desktop ${QT_BUILD_VERSION} win64_msvc2022_64
  set(QT_BUILD_COMPILER "msvc2022_64")
elseif(LINUX)
  # TODO oversimplify : compilation HOST arch = TARGET arch
  if ("${CMAKE_HOST_SYSTEM_PROCESSOR}" STREQUAL "x86_64")
    # python -m aqt install-qt -O build linux desktop ${QT_BUILD_VERSION} linux_gcc_64 (x64)
    set(QT_BUILD_COMPILER "gcc_arm64")
  endif()

  if ("${CMAKE_HOST_SYSTEM_PROCESSOR}" STREQUAL "arm64")
    # python -m aqt install-qt -O build linux_arm desktop ${QT_BUILD_VERSION} linux_gcc_arm64 (arm64)
    set(QT_BUILD_COMPILER "gcc_arm64")
  endif()
elseif(APPLE)
  # python -m aqt install-qt -O build mac desktop ${QT_BUILD_VERSION} clang_64
  set(QT_BUILD_COMPILER "macos")
endif()

if(NOT "${QT_BUILD_COMPILER}")
  message(FATAL "Invalid Qt compiler setting")
endif()

set(Qt6_DIR "${ROOT_DIR}/build/${QT_BUILD_VERSION}/${QT_BUILD_COMPILER}/lib/cmake/Qt6")
set(QT_DIR ${Qt6_DIR})
list(APPEND CMAKE_MODULE_PATH ${Qt6_DIR})

find_package(Qt6 REQUIRED COMPONENTS Core Qml Concurrent)

FetchContent_Declare(
  DieLibrary
  GIT_REPOSITORY "https://github.com/horsicq/die_library"
  GIT_TAG 80e05f3dd3b4fdd287bee0d98d1f27ced324aac0
)

set(DIE_BUILD_AS_STATIC ON CACHE INTERNAL "")
FetchContent_MakeAvailable( DieLibrary )

message(STATUS "Using DieLibrary in '${dielibrary_SOURCE_DIR}'")

list(APPEND CMAKE_MODULE_PATH "${dielibrary_SOURCE_DIR}/dep/build_tools/cmake")
