import socket
import pickle
import jsonpickle
import select
import sys
import time
import random
import sys
from packet import Packet


def channel(c_s_in_port, c_s_out_port, c_r_in_port, c_r_out_port, s_in_port, r_in_port, loss_rate):
    host = '127.0.0.1'


    s_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_in.bind((host, c_s_in_port))

    s_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_out.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_out.bind((host, c_s_out_port))

    r_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    r_in.bind((host, c_r_in_port))

    r_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r_out.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    r_out.bind((host, c_r_out_port))

    print("Channel ports successfully initialised/bound")

    s_in.listen(5)
    print("Listening for sender...")
    
    s_in_connection, s_in_conn_address = s_in.accept()
    print('Got connection from sender: {}'.format(s_in_conn_address))
    time.sleep(0.5)
    s_out.connect((host, s_in_port))
    print("Channel connected to {}".format(c_s_in_port))
    
    r_in.listen(5)
    print("Listening for receiver...")
    r_in_connection, r_in_conn_address = r_in.accept()
    print('Got connection from receiver: {}'.format(r_in_conn_address))
    time.sleep(0.5)
    r_out.connect((host, r_in_port))
    print("Connected to receiver")

    received_message_s = False
    final_packet = False
    while True:
        error_added = False
        ready = select.select([s_in_connection, r_in_connection], [], [], 1);
        
        if ready[0]:
            # Packet received from s_in. Forward to r_out.
            if ready[0][0] is s_in_connection:
                
                # Receive the pakcet & unpickle
                packet_to_fwd = s_in_connection.recv(2048)
                unpickled_packet_to_fwd = pickle.loads(packet_to_fwd)
                
                # Print out details
                print('Sender -> Receiver; Type {}'.format(unpickled_packet_to_fwd.get_packet_type()))
                
                # Check magicNo
                if unpickled_packet_to_fwd.get_magic_no() != 0x497E:
                    continue
                    
                # Chance to drop packet (from loss_rate)
                rand_num_u = random.uniform(0, 1)
                if rand_num_u < loss_rate:
                    # Drop the packet and do not forward
                    print("    Packet lost, retransmitting")
                    continue
                                 
                                 
                # Add the bit error error         
                rand_num_v = random.uniform(0, 1)                
                if rand_num_v < 0.1:
                    
                    #unpickle, change, pickle
                    data_len_increment = random.randint(1, 10)
                    current_data_len = unpickled_packet_to_fwd.get_data_len()
                    unpickled_packet_to_fwd.set_data_len(current_data_len + data_len_increment)
                    print("    Adding bit error of {}".format(data_len_increment))
                                     
                # Pickle it up again
                bytestream_packet = Packet.packet_to_bytes(unpickled_packet_to_fwd)
                bytestream_packets_buffer = []
                bytestream_packets_buffer.append(bytestream_packet)
                error_added = True
                r_out.send(bytestream_packets_buffer[0])
                                 
                
               
            elif ready[0][0] is r_in_connection:
                
                # Receive the pakcet & unpickle
                packet_to_fwd = r_in_connection.recv(2048)
                unpickled_packet_to_fwd = Packet.bytes_to_packet(packet_to_fwd)
                
                # Print out details
                print('Sender <- Receiver; Type {}'.format(unpickled_packet_to_fwd.get_packet_type()))
                      
                # Check magicNo
                if unpickled_packet_to_fwd.get_magic_no() != 0x497E:
                    continue
                
                # If last packet recveived
                if unpickled_packet_to_fwd.get_packet_sequence_no() == 0:
                    print("    Last packet received, terminating channel")
                    break
                    
                # Chance to drop packet (from loss_rate)
                rand_num_u = random.uniform(0, 1)
                if rand_num_u < loss_rate:
                    # Drop the packet and do not forward
                    print("    Packet lost, retransmitting")
                    continue
                                 
                                 
                # Add the bit error error         
                rand_num_v = random.uniform(0, 1)                
                if rand_num_v < 0.1:
                    
                    #unpickle, change, pickle
                    data_len_increment = random.randint(1, 10)
                    current_data_len = unpickled_packet_to_fwd.get_data_len()
                    unpickled_packet_to_fwd.set_data_len(current_data_len + data_len_increment)
                    print("    Adding bit error of {}".format(data_len_increment))
                                     
                # Pickle it up again
                bytestream_packet = Packet.packet_to_bytes(unpickled_packet_to_fwd)
                bytestream_packets_buffer = []
                bytestream_packets_buffer.append(bytestream_packet)
                error_added = True
                s_out.send(bytestream_packets_buffer[0])  
                
                
    s_in.close()
    s_out.close()
    r_in.close()
    r_out.close()
    print("Channel addresses closed")
    

def check_ports(*args):
    for port in args:
        if not isinstance(port, int) or port < 1024 or port > 64000:
            raise Exception("Channel: Invalid port assignments")


def main():
    if len(sys.argv) != 8:
        print("Usage: channel.py <c_s_in_port> <c_s_out_port> <c_r_in_port> <c_r_out_port> <s_in_port> <r_in_port> <loss_rate>")
        exit()

    check_ports(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]))
    
    # Check loss rate
    if float(sys.argv[7]) > 1.0 or float(sys.argv[7]) < 0.0:
        raise Exception("Channel: Loss rate invalid (Must be 0 < P < 1)")
    channel(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), float(sys.argv[7]))

    # channel 42069 42070 42073 42074 42071 0.1
    # sender 42075 42068 42069 access.log
    # receiver 42071 42072 42073 outputfile.txt
    

main()