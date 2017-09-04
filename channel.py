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
        
        
        
        print("r_IN_out s_in_out successfully initialised/bound")
            
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


    def receiveMessageSender(self):
        print("Listening for sender...")
    
        self.s_IN.listen(5)
        
        receivedMessage_s = False
        
        
        while not receivedMessage_s:
            conn, addr = self.s_IN.accept() 
            
            print('Got connection from {}'.format(addr))
            
            #Receives message from sender
            data = conn.recv(1024)
            data = pickle.loads(data)
            if not data:
                print("No data or empty packet received!")
                break
            print("Received; Packet payload:{}\n".format(data.getPacketPayload()))
            receivedMessage_s = True
            
        
        
        return data
        
    def receiveMessageReceiver(self):
        conn, addr = self.r_IN.accept()
        print("Listening for receiver...")
        self.r_IN.listen(5)
        
        recievedMessage_r = False
        
        while not receivedMessage_r:
            conn_r, addr_r = self.r_IN.accept()
        
            print('Got connection from {}'.format(addr))
            data = conn.recv(1024)
            data = pickle.loads(data)
            if not data:
                print("No data or empty packet received!")
                break
            receivedMessage_r = True
        
        
        return data
        
    
    def getHost(self):
        return self.host

def main():
    
    
    channelServer = Channel(42069, 42070, 42073, 42074)
    dataIn = channelServer.receiveMessage()
    
   # trialPacket = Packet(1, 1, 1, "gottem")
    channelServer.sendPacket(42071, data)
    dataOut = channelServer.receiveMessage()
    channelServer.sendPacket(42075, data)
    

main()