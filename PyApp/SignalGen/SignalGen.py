import fprime_pybind
import Fw
import PyApp

class SignalGen(fprime_pybind.SignalGenBase):
    """ Signal Generation in Python """
    def __init__(self):
        """ """
        self.running = False
        self.count = 0


    def schedIn_handler(self, portNum, context):
        """"""
        if self.running:
            self.count = self.count + 1
        pair = PyApp.SignalPair(123, 345)
        self.tlmWrite_PairOutput(pair)

    def SignalGen_Toggle_cmdHandler(self, opCode, cmdSeq):
        """
        :param opCode: Opcode of command executing
        :param cmdSeq: Sequence token
        """
        self.running = True
        self.SignalGen.cmdResponse_out(opCode, cmdSeq, Fw.CommandResponse.COMMAND_OK)

