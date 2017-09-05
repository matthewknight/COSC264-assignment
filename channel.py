import socket
import pickle
from packet import Packet


def channel(c_s_in_port, c_s_out_port, c_r_in_port, c_r_out_port, s_in_port, r_in_port, loss_rate):
    host = '127.0.0.1'

    check_ports(c_s_in_port, c_s_out_port, c_r_in_port, c_r_out_port, s_in_port, r_in_port)

    s_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_in.bind((host, c_s_in_port))

    s_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_out.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_out.bind((host, c_s_in_port))

    r_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    r_in.bind((host, c_r_in_port))

    r_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r_out.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    r_out.bind((host, c_r_out_port))

    print("Channel ports successfully initialised/bound")

    print("Listening for sender...")

    s_in.listen(5)
    s_in_connection, s_in_conn_address = s_in.accept()
    print('Got connection from {}'.format(s_in_conn_address))

    s_out.connect((host, s_in_port))
    print("Channel connected to {}".format(c_s_in_port))

    received_message_s = False

    while not received_message_s:
        # Receives message from sender
        data = s_in_connection.recv(1024)
        data = pickle.loads(data)
        return_no = data.get_packet_sequence_no()
        if data.get_data_len() == 0:
            print("No data or empty packet received!")
            received_message_s = True
        else:
            print("Received; seqno:{}\n".format(data.get_packet_sequence_no()))
            # Send acknowledgement packet

            acknowledgement_packet = Packet(0x497E, 1, return_no, 0, None)

            bytestream_packet = pickle.dumps(acknowledgement_packet)
            s_out.send(bytestream_packet)



def check_ports(*args):
    for port in args:
        if not isinstance(port, int) or port < 1024 or port > 64000:
            raise Exception("Channel: Invalid port assignments")


def main():
    channel(42069, 42070, 42074, 42073, 42075, 42071, 0)

    

main()