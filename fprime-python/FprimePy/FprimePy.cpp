#include <fprime-python/FprimePy/FprimePy.hpp>
#include <Fw/Time/Time.hpp>
#include <Fw/Cmd/CmdResponsePortAc.hpp>

namespace FprimePy {
    py::scoped_interpreter* interpreter;

    void initialize() {
        interpreter = new py::scoped_interpreter();
        py::module_ module = py::module_::import("sys");
        py::print("[FprimePy] Python Interpreter Initialized"); 
        py::print("[FprimePy] PYTHONPATH set to:", module.attr("path")); 
    }

    void destroy() {
        delete interpreter;
    }
};

// Hand-coded framework bindings for fun and profit
PYBIND11_EMBEDDED_MODULE(Fw, m) {
    py::class_<Fw::Time>(m, "Time");
    py::enum_<Fw::CommandResponse>(m, "CommandResponse")
        .value("COMMAND_OK", Fw::COMMAND_OK)
        .value("COMMAND_INVALID_OPCODE", Fw::COMMAND_INVALID_OPCODE)
        .value("COMMAND_VALIDATION_ERROR", Fw::COMMAND_VALIDATION_ERROR)
        .value("COMMAND_FORMAT_ERROR", Fw::COMMAND_FORMAT_ERROR)
        .value("COMMAND_EXECUTION_ERROR", Fw::COMMAND_EXECUTION_ERROR)
        .value("COMMAND_BUSY", Fw::COMMAND_BUSY)
        .export_values();
}
