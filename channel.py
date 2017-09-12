import socket
import pickle
import select
import random
from packet import Packet


def channel(c_s_in_port, c_s_out_port, c_r_in_port, c_r_out_port, s_in_port, r_in_port, loss_rate):
    host = '127.0.0.1'

    check_ports(c_s_in_port, c_s_out_port, c_r_in_port, c_r_out_port, s_in_port, r_in_port)

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

    s_out.connect((host, s_in_port))
    print("Channel connected to {}".format(c_s_in_port))
    
    r_in.listen(5)
    print("Listening for receiver...")
    r_in_connection, r_in_conn_address = r_in.accept()
    print('Got connection from receiver: {}'.format(r_in_conn_address))
    
    r_out.connect((host, r_in_port))
    print("Connected to receiver")

    received_message_s = False

    while True:
        error_added = False
        ready = select.select([s_in_connection, r_in_connection], [], [], 1);
        
        if ready[0]:
            if ready[0][0] is s_in_connection:
                #ADD THE ERROR
                
                
                packet_to_fwd = s_in_connection.recv(1024)
                #ADD THE PACKET LOSS ERROR
                rand_num_u = random.uniform(0, 1)
                if rand_num_u < loss_rate:
                    print("packet lost, retransmitting")
                    break
                                 
                                 
                #Add the bit error error         
                rand_num_v = random.uniform(0, 1)                
                if rand_num_v < 0.1:
                    print("adding bit error")
                    #unpickle, change, pickle
                    unpickle_error = pickle.loads(packet_to_fwd)
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
                #reciever send ackn to sender
                packet_to_fwd = r_in_connection.recv(1024)
                rand_num_u = random.uniform(0, 1)
                if rand_num_u < loss_rate:
                    print("packet lost, retransmitting")
                    break
                                 
                                 
                #Add the bit error error
                                 
                rand_num_v = random.uniform(0, 1)                
                if rand_num_v < 0.1:
                    #unpickle, change, pickle
                    unpickle_error = pickle.loads(packet_to_fwd)
                    unpickle_error.set_data_len(random.randint(1, 10))
                                     
                    #pickle it up again
                    bytestream_packet = pickle.dumps(unpickle_error)
                    bytestream_packets_buffer = []
                    bytestream_packets_buffer.append(bytestream_packet)
                    error_added = True
                    r_out.send(bytestream_packets_buffer[0])
                    
                if not error_added:
                    s_out.send(packet_to_fwd)
            
    s_in.close()
    s_out.close()
    r_in.close()
    r_out.close()

def check_ports(*args):
    for port in args:
        if not isinstance(port, int) or port < 1024 or port > 64000:
            raise Exception("Channel: Invalid port assignments")


def main():
    channel(42069, 42070, 42073, 42074, 42075, 42071, 0)

    

main()