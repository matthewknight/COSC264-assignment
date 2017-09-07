import sys
import time
import pickle
import select
from packet import Packet


def sender(s_in_port, s_out_port, c_s_in_port, file_name):
    import socket
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
            packet_to_send = Packet(0x497E, 0, bytes_read, 0, None)
            exit_flag = True
        else:
            packet_to_send = Packet(0x497E, 0, sequence_no, len(data_read), data_read)
            bytes_position += 512


        bytestream_packet = pickle.dumps(packet_to_send)

        bytestream_packets_buffer.append(bytestream_packet)

        confirmation_received = False

        while not confirmation_received:
            s_out.send(bytestream_packets_buffer[0])
            #time.sleep(0.01)
            ready = select.select([s_in_connection], [], [], 1)
            if ready[0]:
                data = s_in_connection.recv(1024)
                data = pickle.loads(data)
                print(data)
                print(data.get_packet_sequence_no(), sequence_no)
                if data.get_packet_sequence_no() == sequence_no:
                    sequence_no += 1
                    bytestream_packets_buffer.pop(0)
                    confirmation_received = True

                else:
                    print("Packet mismatch, retransmitting")


def check_ports(*args):
    for port in args:
        if not isinstance(port, int) or port < 1024 or port > 64000:
            raise Exception("Channel: Invalid port assignments")


def main():
    sender(42075, 42068, 42069, "access.log")
    
main()
