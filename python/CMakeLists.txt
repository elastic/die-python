project(
    die-python
    LANGUAGES CXX
    VERSION 0.1.0
)

find_package(Python 3
    REQUIRED COMPONENTS Interpreter Development.Module
    OPTIONAL_COMPONENTS Development.SABIModule
)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

execute_process(
    COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
    OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE NB_DIR)
list(APPEND CMAKE_PREFIX_PATH "${NB_DIR}")

find_package(nanobind CONFIG REQUIRED)
find_package(DieLibrary REQUIRED)

set(DIE_PYTHON_ROOT_DIR ${DIE_ROOT_DIR}/python)
set(DIE_BASE_ROOT ${dielibrary_SOURCE_DIR})

nanobind_add_module(_die
    NB_STATIC
        ./src/die.cpp
)

add_dependencies(_die die)

target_include_directories(
    _die
    PRIVATE
        ${DIE_PYTHON_ROOT_DIR}/inc
        ${DIE_BASE_ROOT}/src/include
)

if(MSVC)
    # Disable MSVC `min` & `max` macros for `die` (breaks Qt)
    target_compile_definitions(die PUBLIC NOMINMAX)
endif()

if(APPLE)
    target_link_libraries(_die PRIVATE dl "-framework CoreFoundation")
endif()

if(LINUX)
    # On Linux, let linker lint elf loader to search for curdir/lib
    target_link_options(_die PRIVATE -Wl,-rpath,$ORIGIN/lib)
endif()

target_link_libraries(_die PRIVATE $<TARGET_FILE:die> $<TARGET_PROPERTY:die,LINK_LIBRARIES>)
target_link_libraries(_die PRIVATE Qt6::Core)
target_link_libraries(_die PRIVATE Qt6::Qml)
target_link_libraries(_die PRIVATE Qt6::Concurrent)
target_link_libraries(_die PRIVATE Qt6::Network)

install(DIRECTORY die DESTINATION .)
install(TARGETS _die DESTINATION die/)
install(TARGETS die DESTINATION die/)
install(DIRECTORY ${DIE_BASE_ROOT}/dep/Detect-It-Easy/db DESTINATION die/db)
install(DIRECTORY ${DIE_BASE_ROOT}/dep/Detect-It-Easy/db_custom DESTINATION die/db)

install(
    DIRECTORY
        ${Qt6_DIR}/../../
    DESTINATION
        die/lib
    FILES_MATCHING
        PATTERN "libQt6Core.*"
        PATTERN "libQt6Qml.*"
        PATTERN "libQt6Concurrent.*"
        PATTERN "libQt6Network.*"
        PATTERN "libicui18n.*"
        PATTERN "libicuuc.*"
        PATTERN "libicudata.*"
        PATTERN "cmake" EXCLUDE
        PATTERN "objects-*" EXCLUDE
        PATTERN "pkgconfig" EXCLUDE
)
