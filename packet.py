class Packet(object):
    def __init__(self, maginco, p_type, seqno, dataLen, data):
        self.maginco = maginco
        self.p_type = p_type
        self.seqno = seqno
        self.dataLen = dataLen
        self.data = data
        
    def getMagicNo(self):
        return self.magicno
    
    def getPacketType(self):
        return self.p_type
    
    def getPacketSequence(self):
        return self.seqno
    
    def getDataLength(self):
        return self.dataLen
    
    def getPacketPayload(self):
        return self.data
        
