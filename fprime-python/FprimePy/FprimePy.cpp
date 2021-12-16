#include <fprime-python/FprimePy/FprimePy.hpp>
#include <Fw/Time/Time.hpp>
#include <Fw/Cmd/CmdResponsePortAc.hpp>
#include <Fw/Comp/QueuedComponentBase.hpp>
#include <Fw/Types/String.hpp>
#include <Fw/Cmd/CmdString.hpp>
#include <Fw/Log/LogString.hpp>
#include <Fw/Tlm/TlmString.hpp>

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
    py::enum_<Fw::QueuedComponentBase::MsgDispatchStatus>(m, "MsgDispatchStatus")
        .value("MSG_DISPATCH_OK", Fw::QueuedComponentBase::MSG_DISPATCH_OK)
        .value("MSG_DISPATCH_EMPTY", Fw::QueuedComponentBase::MSG_DISPATCH_EMPTY)
        .value("MSG_DISPATCH_ERROR", Fw::QueuedComponentBase::MSG_DISPATCH_ERROR)
        .value("MSG_DISPATCH_EXIT", Fw::QueuedComponentBase::MSG_DISPATCH_EXIT)
        .export_values();

    py::class_<Fw::String>(m, "String")
            .def(py::init<char *>());
    py::class_<Fw::LogStringArg>(m, "LogStringArg")
            .def(py::init<char *>());
    py::class_<Fw::TlmString>(m, "TlmString")
            .def(py::init<char *>());
    py::class_<Fw::CmdStringArg>(m, "CmdStringArg")
            .def(py::init<char *>());
}
