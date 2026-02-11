project(
    die-python
    LANGUAGES CXX
    VERSION 0.5.1
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
set(DIELIB_BASE_ROOT ${dielibrary_SOURCE_DIR})
set(DIE_BASE_ROOT "${dielibrary_SOURCE_DIR}/dep/Detect-It-Easy")

file(STRINGS ${DIELIB_BASE_ROOT}/release_version.txt DIELIB_VERSION)
file(STRINGS ${DIE_BASE_ROOT}/die_version.txt DIE_VERSION)

nanobind_add_module(_die
        ./src/die.cpp
)

add_dependencies(_die die)

target_include_directories(
    _die
    PRIVATE
        ${DIE_PYTHON_ROOT_DIR}/inc
        ${DIELIB_BASE_ROOT}/src/include
)

if(MSVC)
    # Disable MSVC `min` & `max` macros for `die` (breaks Qt)
    target_compile_definitions(die PUBLIC NOMINMAX)
endif()

if(APPLE)
    target_link_libraries(_die PRIVATE dl "-framework CoreFoundation")
    target_link_options(_die PRIVATE -Wl,-rpath,$ORIGIN/lib)
endif()

if(LINUX)
    target_link_options(_die PRIVATE -Wl,-rpath,$ORIGIN/lib)
endif()

target_compile_definitions(_die
    PRIVATE
        DIE_VERSION="${DIE_VERSION}"
        DIELIB_VERSION="${DIELIB_VERSION}"
)

target_link_libraries(_die PRIVATE $<TARGET_FILE:die> $<TARGET_PROPERTY:die,LINK_LIBRARIES>)
target_link_libraries(_die PRIVATE Qt6::Core)
target_link_libraries(_die PRIVATE Qt6::Qml)
target_link_libraries(_die PRIVATE Qt6::Concurrent)
target_link_libraries(_die PRIVATE Qt6::Network)

# Workaround: die_library on Windows installs files to incorrect locations.
# Remove these before our correct install rules:
# - db/ directory (should be die/db, not site-packages/db)
# - die.lib (should be die/die.lib, not root die.lib)
# - include/ directory (C++ headers not needed in Python wheel)
if(WIN32)
    install(CODE [[
        # List of paths to remove: each entry is "type|path"
        # type: "dir" for directory, "file" for file
        set(REMOVE_PATHS
            "dir|${CMAKE_INSTALL_PREFIX}/db"
            "file|${CMAKE_INSTALL_PREFIX}/die.lib"
            "dir|${CMAKE_INSTALL_PREFIX}/include"
        )

        foreach(REMOVE_ENTRY ${REMOVE_PATHS})
            string(REPLACE "|" ";" REMOVE_LIST "${REMOVE_ENTRY}")
            list(GET REMOVE_LIST 0 REMOVE_TYPE)
            list(GET REMOVE_LIST 1 REMOVE_PATH)

            if(EXISTS "${REMOVE_PATH}")
                if(REMOVE_TYPE STREQUAL "dir")
                    execute_process(COMMAND ${CMAKE_COMMAND} -E remove_directory "${REMOVE_PATH}")
                    message(STATUS "Removed directory: ${REMOVE_PATH}")
                elseif(REMOVE_TYPE STREQUAL "file")
                    execute_process(COMMAND ${CMAKE_COMMAND} -E remove "${REMOVE_PATH}")
                    message(STATUS "Removed file: ${REMOVE_PATH}")
                endif()
            endif()
        endforeach()
    ]])
endif()

install(DIRECTORY die DESTINATION .)
install(TARGETS _die DESTINATION die/)
install(TARGETS die DESTINATION die/)
# Fix: Install database to die/db instead of die/db/db
install(DIRECTORY ${DIELIB_BASE_ROOT}/dep/Detect-It-Easy/db DESTINATION die)
install(DIRECTORY ${DIELIB_BASE_ROOT}/dep/Detect-It-Easy/db_custom DESTINATION die)

if(LINUX OR APPLE)
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
else()
    # Windows: Install Qt DLLs and ICU libraries
    install(
        DIRECTORY
            ${Qt6_DIR}/../../../bin/
        DESTINATION
            die/
        FILES_MATCHING
            PATTERN "Qt6Core.*"
            PATTERN "Qt6Qml.*"
            PATTERN "Qt6Concurrent.*"
            PATTERN "Qt6Network.*"
            PATTERN "icudt*.dll"
            PATTERN "icuin*.dll"
            PATTERN "icuuc*.dll"
    )
endif()