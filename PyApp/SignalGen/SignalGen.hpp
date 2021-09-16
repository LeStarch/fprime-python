// ======================================================================
// \title  SignalGen.hpp
// \author bocchino
// \brief  hpp file for SequenceFileLoader component implementation class
//
// \copyright
// Copyright (C) 2009-2016 California Institute of Technology.
// ALL RIGHTS RESERVED.  United States Government Sponsorship
// acknowledged.
//
// ======================================================================

#ifndef Svc_SignalGen_HPP
#define Svc_SignalGen_HPP

#include <Fw/Types/ByteArray.hpp>
#include <Fw/Types/ConstByteArray.hpp>
#include <Os/File.hpp>
#include <Os/ValidateFile.hpp>
#include <PyApp/SignalGen/SignalGenComponentAc.hpp>
#include <cmath>
#include <fprime-python/PyInit/PyInit.hpp>

namespace PyApp {

class SignalGen : public SignalGenComponentBase {
  private:
    void schedIn_handler(NATIVE_INT_TYPE portNum, /*!< The port number*/
                         NATIVE_UINT_TYPE context /*!< The call order*/
    );

  public:
//    void cmdResponse_out(U32 opCode, U32 cmdSeq, int response);
    /*void SignalGen_Settings_cmdHandler(
        FwOpcodeType opCode,
        U32 cmdSeq,
        U32 Frequency,
        F32 Amplitude,
        F32 Phase,
        PyApp::SignalType SigType
    );*/

    void SignalGen_Toggle_cmdHandler(FwOpcodeType opCode, /*!< The opcode*/
                                     U32 cmdSeq           /*!< The command sequence number*/
    );

    /*void SignalGen_GenerateArray_cmdHandler(
        FwOpcodeType opCode,
        U32 cmdSeq
    );*/

  public:
    //! Construct a SignalGen
    SignalGen(const char* compName  //!< The component name
    );

    //! Initialize a SignalGen
    void init(const NATIVE_INT_TYPE queueDepth,  //!< The queue depth
              const NATIVE_INT_TYPE instance     //!< The instance number
    );

    //! Destroy a SignalGen
    ~SignalGen(void);

    //static PyObject* Inf_cmdResponse_out(PyObject* self, PyObject* args);

    private:
        py::object m_self;
};
};  // namespace PyApp
#endif
