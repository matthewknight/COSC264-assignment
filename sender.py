import sys
import time
import pickle
import jsonpickle
import select
import socket
from packet import Packet
import socket

def sender(s_in_port, s_out_port, c_s_in_port, file_name):
    
    host = '127.0.0.1'

    check_ports(s_in_port, s_out_port, c_s_in_port)

    s_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_in.bind((host, s_in_port))

    s_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_out.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_out.bind((host, s_out_port))
    print("Channel ports successfully initialised/bound")

    s_out.connect((host, c_s_in_port))
    print("Sender connected to {}".format(c_s_in_port))

    s_in.listen(5)
    s_in_connection, s_in_conn_address = s_in.accept()
    print('Got connection from {}'.format(s_in_conn_address))

    bytes_read = 0
    bytes_position = 0
    exit_flag = False
    exit_flag2 = False

    sequence_no = 1
    bytestream_packets_buffer = []

    try:
        file_to_send = open(file_name, 'rb')
    except IOError:
        exit()

    while not exit_flag:
        file_to_send.seek(bytes_position)
        data_read = file_to_send.read(512)

        print(bytes_position)
        if len(data_read) == 0:
            sequence_no = 0
            packet_to_send = Packet(0x497E, 0, sequence_no, 0, None)
            exit_flag = True
            
        else:
            packet_to_send = Packet(0x497E, 0, sequence_no, len(data_read), data_read)
            bytes_position += 512

        print(packet_to_send)
        bytestream_packet = Packet.packet_to_bytes(packet_to_send)

        bytestream_packets_buffer.append(bytestream_packet)

        confirmation_received = False

        while not confirmation_received:
            s_out.send(bytestream_packets_buffer[0])
            print("Ready to send packet")
           
            ready = select.select([s_in_connection], [], [], 1)
            if ready[0]:
                data = s_in_connection.recv(2048)
                data = Packet.bytes_to_packet(data)
                print(data)
                print(data.get_packet_sequence_no(), sequence_no)
                if data.get_packet_sequence_no() == sequence_no:
                    sequence_no += 1
                    bytestream_packets_buffer.pop(0)
                    confirmation_received = True

                else:
                    print("Packet mismatch, retransmitting")

    s_in.close()
    s_out.close()
    print("Sender addresses closed")

def check_ports(*args):
    for port in args:
        if not isinstance(port, int) or port < 1024 or port > 64000:
            raise Exception("Channel: Invalid port assignments")


def main():

    
    if len(sys.argv) != 5:
        print("Usage: sender.py <s_in_port> <s_out_port> <c_s_in_port> <inputfile>")
        exit()
    
    check_ports(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
        
    
    sender(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])    
    
main()
