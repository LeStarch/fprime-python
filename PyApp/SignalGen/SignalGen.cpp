// ======================================================================
// \title  SequenceFileLoader.cpp
// \author bocchino
// \brief  cpp file for SequenceFileLoader component implementation class
//
// \copyright
// Copyright (C) 2009-2016 California Institute of Technology.
// ALL RIGHTS RESERVED.  United States Government Sponsorship
// acknowledged.
//
// ======================================================================

#include <unistd.h>
#include <Fw/Types/Assert.hpp>
#include <PyApp/SignalGen/SignalGen.hpp>



//py::scoped_interpreter guard{};


/* Return the number of arguments of the application command line */
/*PyObject* PyApp::SignalGen::Inf_cmdResponse_out(PyObject* self, PyObject* args) {
    PyObject* object;
    Fw::CommandResponse status;
    U32 opcode = 0;
    U32 seq = 0;
    U64 pointer = 0;

    if (!PyArg_ParseTuple(args, "Liii:Inf_cmdResponse_out", &pointer, &opcode, &seq, &status)) {
        return NULL;
    }
    printf("THIS 3: %lx %lu %lu %lu\n", pointer, opcode, seq, status);
    reinterpret_cast<PyApp::SignalGen*>(pointer)->cmdResponse_out(opcode, seq, status);
    Py_RETURN_NONE;
}

static PyMethodDef SignalGenMethods[] = {
    {"cmdResponse_out", PyApp::SignalGen::Inf_cmdResponse_out, METH_VARARGS, "Category V magic"},
    {NULL, NULL, 0, NULL}};

static PyModuleDef SignalGenModule = {
    PyModuleDef_HEAD_INIT, "SignalGenInf", NULL, -1, SignalGenMethods, NULL, NULL, NULL, NULL};

static PyObject* PyInit_SignalGenInf(void) {
    return PyModule_Create(&SignalGenModule);
}*/

void do_nothing() {}


class SignalGenPublic : public PyApp::SignalGen { // helper type for exposing protected functions
  public:
    using PyApp::SignalGen::cmdResponse_out; // inherited with different access modifier
    using PyApp::SignalGen::tlmWrite_PairOutput; // inherited with different access modifier
};

PYBIND11_EMBEDDED_MODULE(SignalGenInf, m) {
    py::class_<Fw::Time>(m, "Time")
        .def(py::init<>());
    py::class_<PyApp::SignalPair>(m, "SignalPair")
        .def(py::init<F32, F32>());
    py::class_<PyApp::SignalGen>(m, "_SignalGen")
        .def("cmdResponse_out", &SignalGenPublic::cmdResponse_out)
        .def("tlmWrite_PairOutput", &SignalGenPublic::tlmWrite_PairOutput,py::arg("arg"), py::arg("_tlmTime") = Fw::Time());
    py::enum_<Fw::CommandResponse>(m, "CommandResponse")
        .value("COMMAND_OK", Fw::COMMAND_OK)
        .value("COMMAND_BUSY", Fw::COMMAND_BUSY)
        .value("COMMAND_EXECUTION_ERROR", Fw::COMMAND_EXECUTION_ERROR)
    .export_values();

//    m.def("abc", &do_nothing);
    //py::class_<PyApp::SignalGen>(m, "_SignalGen")
    //    .def("schedIn_handler", &PyApp::SignalGen::cmdResponse_out);
    //.def("getName", &Pet::getName);
}
static py::scoped_interpreter guard{};
//py::PY_
static py::gil_scoped_release release;

namespace PyApp {
//PyObject* module = NULL;
// ----------------------------------------------------------------------
// Construction, initialization, and destruction
// ----------------------------------------------------------------------

SignalGen ::SignalGen(const char* name) : SignalGenComponentBase(name) {
}

void SignalGen ::init(const NATIVE_INT_TYPE queueDepth, const NATIVE_INT_TYPE instance) {
    py::gil_scoped_acquire aquire;
    py::module_ module = py::module_::import("SignalGen");
    this->m_self = module.attr("SignalGen")(this);
    SignalGenComponentBase::init(queueDepth, instance);
}

SignalGen ::~SignalGen(void) {}

// ----------------------------------------------------------------------
// Handler implementations
// ----------------------------------------------------------------------

/*void SignalGen ::cmdResponse_out(U32 opCode, U32 cmdSeq, int response) {
    SignalGenComponentBase::cmdResponse_out(opCode, cmdSeq, Fw::COMMAND_OK);
}*/

void SignalGen ::schedIn_handler(NATIVE_INT_TYPE portNum, /*!< The port number*/
                                 NATIVE_UINT_TYPE context /*!< The call order*/
) {
    py::gil_scoped_acquire aquire;
    m_self.attr("schedIn_handler")(portNum, context);
}




/*  void SignalGen :: SignalGen_Settings_cmdHandler(
        FwOpcodeType opCode,
        U32 cmdSeq,
        U32 Frequency,
        F32 Amplitude,
        F32 Phase,
        PyApp::SignalType SigType
    )
  {
      this->signalFrequency = Frequency;
      this->signalAmplitude = Amplitude;
      this->signalPhase     = Phase;
      this->sigType = SigType;

      this->log_ACTIVITY_LO_SignalGen_SettingsChanged(this->signalFrequency, this->signalAmplitude, this->signalPhase,
  this->sigType); this->tlmWrite_Type(SigType); this->cmdResponse_out(opCode, cmdSeq, Fw::COMMAND_OK);
  }*/

void SignalGen ::SignalGen_Toggle_cmdHandler(FwOpcodeType opCode, /*!< The opcode*/
                                             U32 cmdSeq           /*!< The command sequence number*/
) {}

};  // namespace PyApp
