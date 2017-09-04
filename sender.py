import socket
import sys
import pickle
from packet import Packet


class Sender(object):
    def __init__(self, s_in_port, s_out_port, c_s_in_port):
        self.host = '127.0.0.1'
        
        check_ports(s_in_port, s_out_port, c_s_in_port)

        self.s_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s_in.bind((self.host, s_in_port))

        self.s_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_out.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s_out.bind((self.host, s_out_port))
        print("Channel ports successfully initialised/bound")

        self.s_out.connect((self.host, c_s_in_port))
        print("Sender connected to {}".format(c_s_in_port))
    
    def send_file(self, file_name):
        next_no = 0
        exitFlag = False

        try:
            file_to_send = open(file_name, 'r')
        except IOError:
            exit()

        bytestream_file = pickle.dumps(file_to_send.read())
        print(bytestream_file[:10])

        packet = Packet(1, 0, next_no, 10, bytestream_file[:10])
        bytestream_packet = pickle.dumps(packet)
        self.s_out.send(bytestream_packet)




def check_ports(self, *args):
    for port in args:
        if not isinstance(port, int) or port < 1024 or port > 64000:
            raise Exception("Channel: Invalid port assignments")


def main():
    sender_client = Sender(42075, 42078, 42069)
    sender_client.send_file("beefstar.txt")
    
main()