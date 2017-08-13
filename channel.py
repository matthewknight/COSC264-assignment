import socket
import sys
import pickle
from packet import Packet


class Channel(object):
    def __init__(self, s_IN_Port, r_OUT_Port, r_IN_Port, s_OUT_Port):
        
        self.host = '127.0.0.1'
        host = self.host
        self.s_IN_Port = s_IN_Port
        self.r_OUT_Port = r_OUT_Port
        self.r_IN_Port = r_IN_Port
        self.s_OUT_Port = s_OUT_Port
               
        
        self.s_IN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_IN.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s_IN.bind((host, s_IN_Port))
        
        self.r_OUT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.r_OUT.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.r_OUT.bind((host, r_OUT_Port))        

        self.r_IN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.r_IN.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.r_IN.bind((host, r_IN_Port))  
        
        self.s_IN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_IN.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s_IN.bind((host, s_IN_Port))        
        
        
        
        print("r_IN successfully initialised/bound")
            
    def sendPacket(self, destPort, packet):
        r_OUT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        r_OUT.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        r_OUT.bind((self.host, self.r_OUT_Port))
        
        r_OUT.connect((self.host, destPort))
        print("Connected to {}".format(destPort))
        
        bytestreamToSend = pickle.dumps(packet)
            
        print("Sent", repr(packet))
        r_OUT.send(bytestreamToSend)       
        
        r_OUT.close

    def receiveMessage(self):
        print("Listening...")
    
        self.r_IN.listen(5)
        receivedMessage = False
        
        while not receivedMessage:
            conn, addr = self.r_IN.accept() 
            
            print('Got connection from {}'.format(addr))
            
            #Receives message from sender
            data = conn.recv(1024)
            data = pickle.loads(data)
            if not data:
                break
            print("Received; Packet payload:{}\n".format(data.getPacketPayload()))
            receivedMessage = True
            
    
    def getHost(self):
        return self.host

def main():
    
    
    receiverServer = Receiver(42071, 42069)
    receiverServer.receiveMessage()
    
    trialPacket = Packet(1, 1, 1, "gottem")
    receiverServer.sendPacket(42070, trialPacket)
    
main()