import socket
import sys

def sender():
    socket_in = socket.socket(AF_INET, SOCKET.SOCK_STREAM)
    
    socket_out = socket.socket(AF_INET, SOCKET.SOCK_STREAM)
    
    
def reciever():
    recieve_in = socket.socket(AF_INET, SOCKET.SOCK_STREAM)

    recieve_out = socket.socket(AF_INET, SOCKET.SOCK_STREAM)
    
    
def channel():
    if len(sys.argv) != 7:
        print("Too many command line arguments!")
        sys.exit
        
        
    channel_s_in = socket.socket(AF_INET, SOCKET.SOCK_STREAM)
    channel_s_in.bind(("", sys.argv[1]))
    
    channel_s_out = socket.socket(AF_INET, SOCKET.SOCK_STREAM)
    channel_s_out.bind(("", sys.argv[2]))

    channel_r_in = socket.socket(AF_INET, SOCKET.SOCK_STREAM)
    channel_r_in.bind(("", sys.argv[3]))
    
    channel_r_out = socket.socket(AF_INET, SOCKET.SOCK_STREAM)
    channel_r_out.bind(("", sys.argv[4]))
    
    
    s_in_port = ('localhost', sys.argv[5])
    r_in_port = ('localhost', sys.argv[6])
    
    packet_loss_rate = float(sys.argv[7])
    
    
    
class Packet(object, maginco, p_type, seqno, dataLen):
    def __init__(self):
        self.maginco = maginco
        self.p_type = p_type
        self.seqno = seqno
        self.dataLen = dataLen
        self.data = data
        
