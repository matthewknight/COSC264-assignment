import socket
import sys
import pickle
from packet import Packet

#Server
def receiver_sockets(r_IN_Port=42069, r_OUT_Port=42071, destPort=42070):
    host = socket.gethostname()
    
    r_IN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r_IN.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    r_IN.bind((host, r_IN_Port))
    
    print("Initialised, listening.")
    
    r_IN.listen(5)
    
    while True:
        r_OUT, addr = r_IN.accept() 
        
        print('Got connection from {}'.format(addr))
        
        #Receives message from sender
        data = r_OUT.recv(1024)
        data = pickle.loads(data)
        if not data:
            break
        print("Received; {}\n".format(data))
          
        
def main():
    receiver_sockets()

main()
