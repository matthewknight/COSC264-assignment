import socket
import os
import select
import os
import sys
import packet
from packet import Packet


def receiver(r_in_port, r_out_port, c_r_in, filename):
    
    
    try:
        os.remove(filename)
    except OSError:
        pass    
    
    file_to_write = open(filename, 'a+b')
    
    host = '127.0.0.1'

    check_ports(r_in_port, r_out_port, c_r_in)

    try:
        r_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        r_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as e:
        raise Exception("Failed to initialise r_in")

    try:
        r_in.bind((host, r_in_port))
    except socket.error as e:
        raise Exception("Failed to bind r_in")

    try:
        r_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        r_out.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as e:
        raise Exception("Failed to initialise r_out")

    try:
        r_out.bind((host, r_out_port))
    except socket.error as e:
        raise Exception("Failed to bind r_out")

    print("Receiver ports successfully initialised/bound")

    r_out.connect((host, c_r_in))
    print("Receiver connected to channel:{}".format(c_r_in))

    
    r_in.listen(5)
    print("Listening for channel...")
    r_in_connection, r_in_conn_address = r_in.accept()
    print('Got connection from channel:{}'.format(r_in_conn_address))

    received_message_c = False
    expected_num = 0

    while not received_message_c:
        ready = select.select([r_in_connection], [], [])
        if ready[0]:
            # Receives message from sender
            print("Packet received")
            data = r_in_connection.recv(8196)

            data = packet.bytes_to_packet(data)
            print(data)
            return_no = data.get_packet_sequence_no()

            if packet.check_packet_checksum(data) == False:
                continue

            if data.get_data_len() == 0:
                print("No data or empty packet received!")
                received_message_c = True

            elif data.get_packet_payload() == None:
                print("All data received, exiting")
                recieved_message_c = True

            else:
                print("Received; packet :{}\n".format(data))
                # Send acknowledgement packet
                file_to_write.write(data.get_packet_payload())

            acknowledgement_packet = Packet(0x497E, 1, return_no, 0, None)

            print('{} {}\n'.format(data.get_packet_sequence_no(), expected_num))

            if expected_num != data.get_packet_sequence_no():
                bytestream_packet = packet.packet_to_bytes(acknowledgement_packet)
                r_out.send(bytestream_packet)
                continue

            expected_num  = 1 - expected_num

            bytestream_packet = packet.packet_to_bytes(acknowledgement_packet)
            r_out.send(bytestream_packet)

    
    r_in.close()
    r_out.close()
    print("Receiver addresses closed")
    

def check_ports(*args):
    for port in args:
        if not isinstance(port, int) or port < 1024 or port > 64000:
            raise Exception("receiver: Invalid port assignments")


def main():

    try:
        os.remove(sys.argv[4])
    except OSError:
        pass

    if len(sys.argv) != 5:
        print("Usage: receiver.py <r_in_port> <r_out_port> <c_r_in> <outputfile>")
        exit()
    
    check_ports(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
        
    
    receiver(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])    
    

main()