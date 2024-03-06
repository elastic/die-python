include( FetchContent )

# find_package(Qt6 REQUIRED COMPONENTS Core)
# qt_standard_project_setup()

find_package(Qt5 REQUIRED COMPONENTS Core)

FetchContent_Declare(
  DieLibrary
  GIT_REPOSITORY "https://github.com/horsicq/die_library"
  GIT_TAG c9dc7476dbab0d145f2b76729ff1c96dc02cbf82
)

FetchContent_MakeAvailable( DieLibrary )

message(STATUS "Using DieLibrary in '${dielibrary_SOURCE_DIR}'")
