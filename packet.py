class Packet(object):
    def __init__(self, maginco, p_type, seqno, dataLen, data):
        self.maginco = maginco
        self.p_type = p_type
        self.seqno = seqno
        self.dataLen = dataLen
        self.data = data
        
