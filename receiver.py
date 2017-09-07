import socket
import pickle
import select
from packet import Packet


def receiver(r_in_port, r_out_port, c_r_in, filename):
    
    file_to_write = open(filename, 'a+')
    
    host = '127.0.0.1'

    check_ports(r_in_port, r_out_port, c_r_in)

    r_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    r_in.bind((host, r_in_port))

    r_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r_out.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    r_out.bind((host, r_out_port))

    print("Receiver ports successfully initialised/bound")

    r_out.connect((host, c_r_in))
    print("Receiver connected to channel:{}".format(c_r_in))

    
    r_in.listen(5)
    print("Listening for channel...")
    r_in_connection, r_in_conn_address = r_in.accept()
    print('Got connection from channel:{}'.format(r_in_conn_address))
    

    
    
    received_message_c = False

    while not received_message_c:
        ready = select.select([r_in_connection], [], [])
        if ready[0]:
            # Receives message from sender
            print("Packet received")
            data = r_in_connection.recv(1024)
            data = pickle.loads(data)
            return_no = data.get_packet_sequence_no()
            if data.get_data_len() == 0:
                print("No data or empty packet received!")
                received_message_c = True
            else:
                print("Received; seqno:{}\n".format(data))
                # Send acknowledgement packet
                file_to_write.write(data.get_packet_payload())
                acknowledgement_packet = Packet(0x497E, 1, return_no, 0, None)
    
                bytestream_packet = pickle.dumps(acknowledgement_packet)
                r_out.send(bytestream_packet)



def check_ports(*args):
    for port in args:
        if not isinstance(port, int) or port < 1024 or port > 64000:
            raise Exception("receiver: Invalid port assignments")


def main():
    receiver(42071, 42072, 42073, "outputfile.txt")

    

main()