import socket
import pickle


class Channel(object):
    def __init__(self, c_s_in_port, c_s_out_port, c_r_in_port, c_r_out_port, s_in_port, r_in_port, loss_rate):
        self.host = '127.0.0.1'
        host = self.host

        check_ports(c_s_in_port, c_s_out_port, c_r_in_port, c_r_out_port, s_in_port, r_in_port)
        
        self.s_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s_in.bind((host, c_s_in_port))

        self.s_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_out.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s_out.bind((host, c_s_in_port))

        self.r_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.r_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.r_in.bind((host, c_r_in_port))

        self.r_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.r_out.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.r_out.bind((host, c_r_out_port))

        self.s_in_port = s_in_port
        self.r_in_port = r_in_port
        self.loss_rate = loss_rate

        print("Channel ports successfully initialised/bound")

    def send_packet(self, destination_port, packet):
        self.r_out.connect((self.host, destination_port))

        print("Connected to {}".format(destination_port))
        
        bytestream_to_send = pickle.dumps(packet)
            
        print("Sent", repr(packet))
        self.r_out.send(bytestream_to_send)
        
        self.r_out.close

    def receive_message_sender(self):
        print("Listening for sender...")
    
        self.s_in.listen(5)
        
        received_message_s = False

        while not received_message_s:
            conn, addr = self.s_in.accept()
            print('Got connection from {}'.format(addr))

            # Receives message from sender
            data = conn.recv(1024)
            data = pickle.loads(data)
            if not data:
                print("No data or empty packet received!")
                break
            else:
                print("Received; Packet payload:{}\n".format(data.getPacketPayload()))
                received_message_s = True
                return data
        
    def receive_message_receiver(self):
        conn, addr = self.r_in.accept()
        print("Listening for receiver...")
        self.r_in.listen(5)
        
        received_message_r = False
        
        while not received_message_r:
            conn_r, addr_r = self.r_in.accept()
        
            print('Got connection from {}'.format(addr))
            data = conn.recv(1024)
            data = pickle.loads(data)
            if not data:
                print("No data or empty packet received!")
                break
            else:
                print("Received; Packet payload:{}\n".format(data.getPacketPayload()))
                received_message_r = True
                return data

    def get_host(self):
        return self.host


def check_ports(self, *args):
    for port in args:
        if not isinstance(port, int) or port < 1024 or port > 64000:
            raise Exception("Channel: Invalid port assignments")


def main():
    channel_server = Channel(42069, 42070, 42074, 42073)
    data_in = channel_server.receiveMessage()
    print(data_in)

    # trialPacket = Packet(1, 1, 1, "gottem")
    # channel_server.send_packet(42071, data)
    # dataOut = channel_server.receiveMessage()
    # channel_server.send_packet(42075, data)
    

main()