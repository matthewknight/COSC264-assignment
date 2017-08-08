import socket
import sys

def client_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 42069
    
    s.connect((host, port))
    print(s.recv(1024))
    s.close
    

client_socket()
