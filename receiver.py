import socket
import sys
import pickle
from packet import Packet

import socket
import sys
import pickle
from packet import Packet

#Server
class Receiver(object):
    def __init__(self, r_OUT_Port, r_IN_Port):
        self.host = socket.gethostname()
        host = self.host
        
        #Check for in range ports
        if (r_OUT_Port < 1024 or r_OUT_Port > 64000):
            print("r_OUT port out of range")
            k=input("Any key to exit")
            exit()
        
        if (r_IN_Port < 1024 or r_IN_Port > 64000):
            print("r_IN port out of range")
            k=input("Any key to exit")
            exit()       
        
        self.r_IN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.r_IN.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.r_IN.bind((host, r_IN_Port))
        print("r_IN successfully initialised/bound")
            
    def sendMessage(self, destPort, message):
        return None

    def receiveMessage(self):
        print("Listening...")
    
        self.r_IN.listen(5)
        #receivedMessage = False
        
        while True:
            r_OUT, addr = self.r_IN.accept() 
            
            print('Got connection from {}'.format(addr))
            
            #Receives message from sender
            data = r_OUT.recv(1024)
            data = pickle.loads(data)
            if not data:
                break
            print("Received; {}\n".format(data))
            
            
    
    def getHost(self):
        return self.host

def main():
    receiverServer = Receiver(42071, 42069)
    receiverServer.receiveMessage()    
    
main()