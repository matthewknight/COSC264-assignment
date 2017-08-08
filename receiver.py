import socket
import sys

#Server
def receiver_socket(r_IN_Port=42069, r_OUT_Port=42071, destPort=42070):
    host = socket.gethostname()
    
    r_IN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r_IN.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    r_IN.bind((host, r_IN_Port))
    
    r_OUT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r_OUT.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    r_OUT.bind((host, r_OUT_Port))
    
    print("Initialised")
    r_IN.listen(5)
    
    while True:
        connection, address = r_IN.accept()
        print('Got connection from {}'.format(address))
        
        #Receives message from sender
        data = r_IN.recv(1024)
        if not data:
            break
        print("Data to forward back to sender; {}\n".format(data))
        
        #Forwards same message back to sender
        r_OUT.connect((host, destPort)) 
        r_OUT.send(data)
        r_OUT.close()    
    
receiver_socket()
