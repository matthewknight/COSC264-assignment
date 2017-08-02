import socket
import sys
import cPickle as pickle

#Copy paste for running command from terminal - 7642 23501 38001 packet.txt

class Packet(object):
    def __init__(self, maginco, p_type, seqno, dataLen, data):
        self.maginco = maginco
        self.p_type = p_type
        self.seqno = seqno
        self.dataLen = dataLen
        self.data = data
        

def sender():
    """
    Takes 4 commands from the command line
    -Two port numbers to use for the two sender sockets
    -One port number to use for the channel socket
    -A file name, indicating the file to send.
    """
    #Checkers for ommand line arguments
    if len(sys.argv) != 5:
        print("ERROR:", len(sys.argv), "argument(s) passed. Please make sure there are 4.")
        sys.exit(0)  
        
    if int(sys.argv[1]) < 1024 or int(sys.argv[2]) < 1024:
        print("Invalid port numbers used. Check numbers and try again.")
        sys.exit(0)  
    
    if int(sys.argv[1]) > 64000 or int(sys.argv[2]) > 64000:
        print("Invalid port numbers used. Check numbers and try again.2")
        sys.exit(0)     
    
    
    socket_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_in.bind(("", int(sys.argv[1])))
    socket_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_out.bind(("", int(sys.argv[2])))
    
    socket_out.connect(('127.0.0.1', 38001))
    socket_out.recvfrom(38001)
    
    
    
def main():
    sender()
    trialPacket = Packet(290137812738912, "IP_NET", 0, 0, 0)
    testFile = open("packet.txt", "w")
    pickle.dump(trialPacket, testFile)

main()
    
    