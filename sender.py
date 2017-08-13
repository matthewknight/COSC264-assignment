import socket
import sys
import pickle
from packet import Packet

#Client
class Sender(object):
    def __init__(self, s_OUT_Port, s_IN_Port):
        self.host = socket.gethostname()
        
        #Check for in range ports
        if (s_OUT_Port < 1024 or s_OUT_Port > 64000):
            print("s_OUT port out of range\n")
            k = input("Any key to exit")
            exit()
            
            
        if (s_IN_Port < 1024 or s_IN_Port > 64000):
            print("s_IN port out of range\n")
            k = input("Any key to exit")
            exit()            
        

        self.s_IN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_IN.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s_IN.bind((self.host, s_IN_Port))

        self.s_OUT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_OUT.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s_OUT.bind((self.host, s_OUT_Port))       
    
    def sendMessage(self, destPort, message):
        self.s_OUT.connect((self.host, destPort))
        print("Connected to {}".format(destPort))
        
        bytestreamToSend = pickle.dumps(message)
            
        print("Sent", repr(message))
        self.s_OUT.send(bytestreamToSend)       
        
        
        self.s_OUT.close()

        
        
    
    def receiveMessage(self):
        return None
    
    def getHost(self):
        return self.host
    
def main():
    senderClient = Sender(42068, 42070)
    senderClient.sendMessage(42069, "deez nuts")
    
main()