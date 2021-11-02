""" SignalGen.py:

Python implementation of the SignalGen fprime component. This component is dependent on autocoded bindings that
map to this component. **Note:** ensure this file is renamed to SignalGen.py in the current folder.
"""
import time
import math
import random

# Required imports for the implementation to work
import fprime_pybind

# Typical, but optional, imports
import Fw
import PyApp

FRACT = lambda x, period: x % period
SIG_FUNCTIONS = {
    PyApp.SignalType.t.TRIANGLE: lambda x, period: FRACT(x, period) if (FRACT(x, period) < period/2) else 1.0 - FRACT(x, period),
    PyApp.SignalType.t.SQUARE: lambda x, period: 1.0 if (FRACT(x) < period/2) else 0.0,
    PyApp.SignalType.t.SINE: lambda x, period: math.sin(2.0 * math.pi * x / period),
    PyApp.SignalType.t.NOISE: lambda x, period: random.random()
}


class SignalGen(fprime_pybind.SignalGenBase):
    """ Implementation of SignalGen component. """

    def __init__(self):
        """ Constructor implementation """
        self.base_time = 0.0
        self.running = False
        self.period = 1.0
        self.amplitude = 1.0
        self.sig_type = PyApp.SignalType.t.SINE
        self.history = [0.0] * 4
        self.pair_history = [PyApp.SignalPair(0.0, 0.0)] * 4

    def schedIn_handler(self, portNum, context):
        """ Port handler for schedIn """
        self.doDispatch()
        if self.running:
            time_as_float = time.time() - self.base_time
            current_value = SIG_FUNCTIONS[self.sig_type](time_as_float, self.period)

            self.tlmWrite_Type(PyApp.SignalType(self.sig_type))
            self.tlmWrite_Output(current_value)

            current_pair = PyApp.SignalPair(time_as_float, math.sin(2 * math.pi * time_as_float))
            self.tlmWrite_PairOutput(current_pair)

            self.history = self.history[1:] + [current_value]
            self.pair_history = self.pair_history[1:] + [current_pair]
            self.tlmWrite_History(PyApp.SignalSet(*self.history))
            pair_history_obj = PyApp.SignalPairSet()
            for index in range(0, PyApp.SignalPairSet.size):
                pair_history_obj[index] = self.pair_history[index]
            self.tlmWrite_PairHistory(pair_history_obj)

            info = PyApp.SignalInfo()
            info.settype(PyApp.SignalType(self.sig_type))
            info.sethistory(PyApp.SignalSet(*self.history))
            info.setpairHistory(pair_history_obj)
            self.tlmWrite_Info(info)

    def Settings_cmdHandler(self, opCode, cmdSeq, Frequency, Amplitude, SigType):
        """ Command handler for SignalGen_Settings """
        self.period = 1 / Frequency
        self.amplitude = Amplitude
        self.sig_type = SigType
        self.cmdResponse_out(opCode, cmdSeq, Fw.CommandResponse.COMMAND_OK)

    def Toggle_cmdHandler(self, opCode, cmdSeq):
        """ Command handler for SignalGen_Toggle """
        self.running = not self.running
        self.base_time = time.time()
        self.cmdResponse_out(opCode, cmdSeq, Fw.CommandResponse.COMMAND_OK)
