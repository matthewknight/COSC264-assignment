import socket
import sys
import pickle
from packet import Packet

#Client
class Sender(object):
    def __init__(self, s_OUT_Port, s_IN_Port):
        self.host = socket.gethostname()
        self.s_OUT_Port = s_OUT_Port
        
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

               
    
    def sendPacket(self, destPort, packet):
        s_OUT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_OUT.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s_OUT.bind((self.host, self.s_OUT_Port))
        
        s_OUT.connect((self.host, destPort))
        print("Connected to {}".format(destPort))
        
        bytestreamToSend = pickle.dumps(packet)
            
        print("Sent", repr(packet))
        s_OUT.send(bytestreamToSend)       
        
        s_OUT.close
        
    def receiveMessage(self):
        print("Listening...")
    
        self.s_IN.listen(5)
        receivedMessage = False
        
        while not receivedMessage:
            conn, addr = self.s_IN.accept() 
            
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
    senderClient = Sender(42068, 42070)
    trialPacket = Packet(1, 1, 1, "deeznutz")
    
    senderClient.sendPacket(42069, trialPacket)
    senderClient.receiveMessage()
    
main()