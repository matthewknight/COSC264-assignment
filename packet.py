class Packet(object):
    def __init__(self, p_type, seqno, dataLen, data):
        self.magicno = 0x497E
        self.p_type = p_type
        self.seqno = seqno
        self.dataLen = dataLen
        self.data = data
        
    def getMagicNo(self):
        return self.magicno
    
    def getPacketType(self):
        #Flag for if connecting packet or final packet (I think??)
        return self.p_type
    
    def getPacketSequence(self):
        return self.seqno
    
    def getDataLength(self):
        return self.dataLen
    
    def getPacketPayload(self):
        return self.data
        
