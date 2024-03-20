include( FetchContent )

find_package(Qt6 REQUIRED COMPONENTS Core Qml)

# if(WIN32)
#   if(CMAKE_SIZEOF_VOID_P EQUAL 8)
#     set(TARGET_URL https://github.com/horsicq/die_library/releases/download/Beta/dielib_win64_portable_3.09_x64.zip)
#     set(TARGET_HASH 7E6F10DC48C9F55043E2502EEF19F9FBB502AD66)
#   elseif(CMAKE_SIZEOF_VOID_P EQUAL 4)
#     set(TARGET_URL https://github.com/horsicq/die_library/releases/download/Beta/dielib_win32_portable_3.09_x86.zip)
#     set(TARGET_HASH D1AA1174CF32AE52D74A5E93CA202D5D03CB973F)
#   endif()
# else()
# endif(WIN32)

FetchContent_Declare(
  DieLibrary
  GIT_REPOSITORY "https://github.com/horsicq/die_library"
  # GIT_TAG c9dc7476dbab0d145f2b76729ff1c96dc02cbf82
  GIT_TAG master
  # URL ${TARGET_URL}
  # URL_HASH SHA1=${TARGET_HASH}
)

FetchContent_MakeAvailable( DieLibrary )

message(STATUS "Using DieLibrary in '${dielibrary_SOURCE_DIR}'")

list(APPEND CMAKE_MODULE_PATH "${dielibrary_SOURCE_DIR}/dep/build_tools/cmake")
