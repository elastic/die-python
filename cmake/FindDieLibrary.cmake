include(FetchContent)

set(ROOT_DIR "${CMAKE_CURRENT_LIST_DIR}/..")

# Only use Qt6

set(QT_BUILD_VERSION "6.7.1")

if(WIN32)
  # python -m aqt  install-qt windows desktop 6.7.1 win64_msvc2019_64
  set(QT_BUILD_COMPILER "msvc2019_64")
  set(Qt6_DIR "${ROOT_DIR}/build/${QT_BUILD_VERSION}/${QT_BUILD_COMPILER}/lib/cmake/Qt6")
  set(QT_DIR ${Qt6_DIR})
  list(APPEND CMAKE_MODULE_PATH ${Qt6_DIR})
endif(WIN32)
# For Linux/MacOS, use the binaries from the system

find_package(Qt6 REQUIRED COMPONENTS Core Qml Concurrent)

FetchContent_Declare(
  DieLibrary
  GIT_REPOSITORY "https://github.com/calladoum-elastic/die_library"
  GIT_TAG af4528ba080ff06060dddd87b1f71bb7aa980af8
)
set(DIE_BUILD_AS_STATIC ON CACHE INTERNAL "")
FetchContent_MakeAvailable( DieLibrary )

message(STATUS "Using DieLibrary in '${dielibrary_SOURCE_DIR}'")

list(APPEND CMAKE_MODULE_PATH "${dielibrary_SOURCE_DIR}/dep/build_tools/cmake")
