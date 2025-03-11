include(FetchContent)

cmake_path(SET ROOT_DIR NORMALIZE "${CMAKE_CURRENT_LIST_DIR}/..")

# Only use Qt6

set(QT_BUILD_VERSION "6.7.3")

# TODO (calladoum) : here we oversimplify by assuming that compilation HOST and TARGET have same architecture

if(WIN32)
  # python -m aqt install-qt -O build windows desktop ${QT_BUILD_VERSION} win64_msvc2022_64
  set(QT_BUILD_COMPILER "msvc2022_64")

elseif(LINUX)
  if (${CMAKE_HOST_SYSTEM_PROCESSOR} STREQUAL "x86_64")
    # python -m aqt install-qt -O build linux desktop ${QT_BUILD_VERSION} linux_gcc_64 (x64)
    set(QT_BUILD_COMPILER "gcc_64")
  endif()

  if (${CMAKE_HOST_SYSTEM_PROCESSOR} STREQUAL "aarch64")
    # python -m aqt install-qt -O build linux_arm desktop ${QT_BUILD_VERSION} linux_gcc_arm64 (arm64)
    set(QT_BUILD_COMPILER "gcc_arm64")
  endif()

elseif(APPLE)
  # python -m aqt install-qt -O build mac desktop ${QT_BUILD_VERSION} clang_64
  set(QT_BUILD_COMPILER "macos")
endif()

if(NOT QT_BUILD_COMPILER)
  message(FATAL_ERROR "Invalid Qt compiler setting")
else()
  message(STATUS "CMAKE_HOST_SYSTEM_PROCESSOR: ${CMAKE_HOST_SYSTEM_PROCESSOR}")
  message(STATUS "QT_BUILD_VERSION: ${QT_BUILD_VERSION}")
  message(STATUS "QT_BUILD_COMPILER: ${QT_BUILD_COMPILER}")
endif()

set(Qt6_CMAKE_ROOT "${ROOT_DIR}/build/${QT_BUILD_VERSION}/${QT_BUILD_COMPILER}/lib/cmake")
set(Qt6_DIR ${Qt6_CMAKE_ROOT}/Qt6)
set(QT_DIR ${Qt6_DIR})

message(STATUS "Qt6_CMAKE_ROOT: ${Qt6_CMAKE_ROOT}")
message(STATUS "Qt6_DIR: ${Qt6_DIR}")

list(INSERT CMAKE_MODULE_PATH 0
  ${Qt6_CMAKE_ROOT}
  ${Qt6_DIR}
)

find_package(Qt6 REQUIRED COMPONENTS Core Qml Concurrent)

FetchContent_Declare(
  DieLibrary
  GIT_REPOSITORY "https://github.com/horsicq/die_library"
  GIT_TAG 09df9ccafe48a0531987ad1e605402ed79d4c3f6
)

set(DIE_BUILD_AS_STATIC ON CACHE INTERNAL "")
FetchContent_MakeAvailable( DieLibrary )

message(STATUS "Using DieLibrary in '${dielibrary_SOURCE_DIR}'")

list(APPEND CMAKE_MODULE_PATH "${dielibrary_SOURCE_DIR}/dep/build_tools/cmake")
