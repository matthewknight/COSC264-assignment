import socket
import pickle
import select
<<<<<<< HEAD
import sys
=======
import time
>>>>>>> 0ce192730be9360be3ba02802fb4146cbf3a6902
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
            if ready[0][0] is s_in_connection:
                #ADD THE ERROR
                
                
                packet_to_fwd = s_in_connection.recv(1024)
                unpickle_error = pickle.loads(packet_to_fwd)
                # If last packet recveived
                
                #check magicno
                if unpickle_error.get_magic_no() != 0x497E:
                    continue
                
                if unpickle_error.get_packet_sequence_no() == 0:
                    final_packet = True
                    print("Last packet received, terminating channel")
                    
                #ADD THE PACKET LOSS ERROR
                rand_num_u = random.uniform(0, 1)
                if rand_num_u < loss_rate:
                    print("packet lost, retransmitting")
                    continue
                                 
                                 
                #Add the bit error error         
                rand_num_v = random.uniform(0, 1)                
                if rand_num_v < 0.1:
                    print("adding bit error")
                    #unpickle, change, pickle
                    
                    unpickle_error.set_data_len(random.randint(1, 10))
                                     
                    #pickle it up again
                    bytestream_packet = pickle.dumps(unpickle_error)
                    bytestream_packets_buffer = []
                    bytestream_packets_buffer.append(bytestream_packet)
                    error_added = True
                    r_out.send(bytestream_packets_buffer[0])
                                 
                #Send to receiver
                if not error_added:
                    r_out.send(packet_to_fwd)                
                
                
                
                
                #Send to receiver
                
               
            elif ready[0][0] is r_in_connection:
                
                packet_to_fwd = r_in_connection.recv(1024)
                unpickle_error = pickle.loads(packet_to_fwd)
                # If last packet recveived
                
                #check magicno
                if unpickle_error.get_magic_no() != 0x497E:
                    continue
                
                if unpickle_error.get_packet_sequence_no() == 0:
                    final_packet = True
                    print("Last packet received, terminating channel")
                    
                #ADD THE PACKET LOSS ERROR
                rand_num_u = random.uniform(0, 1)
                if rand_num_u < loss_rate:
                    print("packet lost, retransmitting")
                    continue
                                 
                                 
                #Add the bit error error         
                rand_num_v = random.uniform(0, 1)                
                if rand_num_v < 0.1:
                    print("adding bit error")
                    #unpickle, change, pickle
                    
                    unpickle_error.set_data_len(random.randint(1, 10))
                                     
                    #pickle it up again
                    bytestream_packet = pickle.dumps(unpickle_error)
                    bytestream_packets_buffer = []
                    bytestream_packets_buffer.append(bytestream_packet)
                    error_added = True
                    s_out.send(bytestream_packets_buffer[0])
                    if final_packet:
                        break                          
                #Send to receiver
                if not error_added:
                    s_out.send(packet_to_fwd)
                    if final_packet:
                        break
            
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
    
<<<<<<< HEAD
=======
    
    
>>>>>>> 0ce192730be9360be3ba02802fb4146cbf3a6902
    

main()