#include <fprime-python/FprimePy/FprimePy.hpp>

namespace FprimePy {
    py::scoped_interpreter* interpreter;
    py::gil_scoped_release* releaser;
    void initialize() {
        interpreter = new py::scoped_interpreter();
        py::module_ module = py::module_::import("sys");
        py::print("[FprimePy] Python Interpreter Initialized"); 
        py::print("[FprimePy] PYTHONPATH set to:", module.attr("path"));
        releaser = new py::gil_scoped_release();
    }

    void destroy() {
        delete releaser;
        delete interpreter;
    }
};