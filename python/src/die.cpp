#include "die.hpp"

#include <nanobind/nanobind.h>
#include <nanobind/stl/array.h>
#include <nanobind/stl/function.h>
#include <nanobind/stl/list.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>

#include <optional>
#include <string>

namespace nb = nanobind;
using namespace nb::literals;

NB_MODULE(_die, m)
{

    nb.enum_<DIE_lib::SF>(m, "SF")
        .value("SF_DEEPSCAN", DIE_lib::SF::SF_DEEPSCAN)
        .value("SF_HEURISTICSCAN", DIE_lib::SF::SF_HEURISTICSCAN)
        .value("SF_ALLTYPESSCAN", DIE_lib::SF::SF_ALLTYPESSCAN)
        .value("SF_RECURSIVESCAN", DIE_lib::SF::SF_RECURSIVESCAN)
        .value("SF_VERBOSE", DIE_lib::SF::SF_VERBOSE)
        .value("SF_RESULTASXML", DIE_lib::SF::SF_RESULTASXML)
        .value("SF_RESULTASJSON", DIE_lib::SF::SF_RESULTASJSON)
        .value("SF_RESULTASTSV", DIE_lib::SF::SF_RESULTASTSV)
        .value("SF_RESULTASCSV", DIE_lib::SF::SF_RESULTASCSV)
        .export_values();

    m.doc()               = "The native `die` module";
    m.attr("__version__") = "0.1.0";
    nb::class_<DIE_libdie>(m, "DIE_lib")
        .def(nb::init<>())
        .def(
            "scanFile",
            [](DIE_lib& t, std::string const& FileName, uint32_t Flags, std::string const& DatabasePath)
                -> std::optional<std::string>
            {
                auto res = t.scanFileA(FileName.c_str(), Flags, DatabasePath);
                if ( !res )
                    return std::nullopt;
                return std::string(res);
            })
        // .def("freeMemoryA", DIE_lib::freeMemoryA, "pszString"_a)
        ;
}