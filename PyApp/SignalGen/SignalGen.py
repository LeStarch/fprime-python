import SignalGenInf

class SignalGenBase(object):

    def __init__(self):
        self.this = None

    def cmdResponse_out(self, opCode, cmdSeq, status):
        tmp = self.this
        print("This 3: {0:x}".format(tmp), opCode, cmdSeq, status)
        SignalGenInf.cmdResponse_out(tmp, opCode, cmdSeq, status)
        #SignalGenInf.cmdResponse_out(cmdSeq, status)


class SignalGen(SignalGenBase):
    """ Signal Generation in Python """
    def __init__(self, this):
        """ """
        super().__init__()
        self.this = this
        self.running = False
        self.count = 0


    def schedIn_handler(self, portNum, context):
        """"""
        print(f"[PYTHON] WAAAAAAAAAAAAAAAAAA: {portNum} with {context} and count: {self.count}")
        if self.running:
            self.count = self.count + 1
        pair = SignalGenInf.SignalPair(123, 345)
        self.this.tlmWrite_PairOutput(pair)
        self.this.cmdResponse_out(2, 3, SignalGenInf.CommandResponse.COMMAND_OK)

    def SignalGen_Toggle_cmdHandler(self, opCode, cmdSeq):
        """
        :param opCode: Opcode of command executing
        :param cmdSeq: Sequence token
        """
        self.running = True
        self.cmdResponse_out(opCode, cmdSeq, 0)

