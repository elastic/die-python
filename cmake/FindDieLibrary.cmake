include( FetchContent )

# find_package(Qt6 REQUIRED COMPONENTS Core)
# qt_standard_project_setup()

# find_package(Qt5 REQUIRED COMPONENTS Core)

if (NOT CMAKE_SYSTEM_PROCESSOR MATCHES "(x86)|(X86)|(amd64)|(AMD64)")
  message(FATAL_ERROR "Only support intel processors")
endif()

if(CMAKE_SIZEOF_VOID_P EQUAL 8)
  set(TARGET_URL https://github.com/horsicq/die_library/releases/download/Beta/dielib_win64_portable_3.09_x64.zip)
  set(TARGET_HASH 7E6F10DC48C9F55043E2502EEF19F9FBB502AD66)
elseif(CMAKE_SIZEOF_VOID_P EQUAL 4)
  set(TARGET_URL https://github.com/horsicq/die_library/releases/download/Beta/dielib_win32_portable_3.09_x86.zip)
  set(TARGET_HASH D1AA1174CF32AE52D74A5E93CA202D5D03CB973F)
endif()

FetchContent_Declare(
  DieLibrary
  # GIT_REPOSITORY "https://github.com/horsicq/die_library"
  # GIT_TAG c9dc7476dbab0d145f2b76729ff1c96dc02cbf82
  URL ${TARGET_URL}
  URL_HASH SHA1=${TARGET_HASH}
)

FetchContent_MakeAvailable( DieLibrary )

message(STATUS "Using DieLibrary in '${dielibrary_SOURCE_DIR}'")
