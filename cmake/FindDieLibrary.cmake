include( FetchContent )

# Only use Qt6
find_package(Qt6 REQUIRED COMPONENTS Core Qml Concurrent)

FetchContent_Declare(
  DieLibrary
  GIT_REPOSITORY "https://github.com/calladoum-elastic/die_library"
  GIT_TAG ff412022d34289115426ba1cb7b8663d728f7bb3
)

FetchContent_MakeAvailable( DieLibrary )

message(STATUS "Using DieLibrary in '${dielibrary_SOURCE_DIR}'")

list(APPEND CMAKE_MODULE_PATH "${dielibrary_SOURCE_DIR}/dep/build_tools/cmake")
