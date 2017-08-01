import socket
import sys

#Default port numbers to use : 38764 21983

def reciever():
    recieve_in = socket.socket(AF_INET, SOCKET.SOCK_STREAM)
    recieve_in.bind(("", 38764))
    recieve_out = socket.socket(AF_INET, SOCKET.SOCK_STREAM)
    recieve_out.bind(("", 21983))