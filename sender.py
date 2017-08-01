import socket
import sys

#Default port values 7642 23501
def sender():
    socket_in = socket.socket(AF_INET, SOCKET.SOCK_STREAM)
    socket_in.bind(("", 7642))
    socket_out = socket.socket(AF_INET, SOCKET.SOCK_STREAM)
    socket_out.bind(("", 23501))