import socket
import sys
import pickle
from packet import Packet

#Client
def sender_main(s_IN_Port=42070, s_OUT_Port=42068, destPort=42069, payload=b"mynamajeff"):
    host = socket.gethostname()
    
    s_IN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_IN.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_IN.bind((host, s_IN_Port))
    
    s_OUT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_OUT.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_OUT.bind((host, s_OUT_Port))

    s_OUT.connect((host, destPort))
    
    print("Connected to {}".format(destPort))
    
    bytestreamToSend = pickle.dumps(payload)
    
    print("Sent", repr(payload))
    s_OUT.send(bytestreamToSend)    
    
    
def main(): 
    trialPacket = Packet(290137812738912, "IP_NET", 0, 0, 0)
    
    sender_main(42070, 42068, 42069, trialPacket)
    
main()