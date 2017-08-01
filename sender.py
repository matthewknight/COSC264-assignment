import socket
import sys
import cPickle as pickle

class Packet(object):
    def __init__(self, maginco, p_type, seqno, dataLen, data):
        self.maginco = maginco
        self.p_type = p_type
        self.seqno = seqno
        self.dataLen = dataLen
        self.data = data
        
#Default port values 7642 23501
def sender():
    socket_in = socket.socket(AF_INET, SOCKET.SOCK_STREAM)
    socket_in.bind(("", 7642))
    socket_out = socket.socket(AF_INET, SOCKET.SOCK_STREAM)
    socket_out.bind(("", 23501))
    
def main():
    trialPacket = Packet(290137812738912, "IP_NET", 0, 0, 0)
    testFile = open("packet.txt", "w")
    pickle.dump(trialPacket, testFile)

main()
    
    