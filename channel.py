import socket
import sys

  
def channel():

    """Takes 7 command line arguments. These are:
       -Four port numbers csin, csout, crin, crout
       -One port number sin socket of sender (To which channel will send packets to sender
       -One port number rin socket of the reciever (To which channel will send packets to reciever.
       -A floating point P which is the Packet Loss Rate. 0 <= P < 1
    """
    
    #Check if all arguments were recieved
    if len(sys.argv) != 7:
        print("Not enough command line arguments passed. Please make sure there are 7.")
        sys.exit
    #Check if all port numbers are valid. 1024 <= port < 64000
    if not (sys.argv[1] > 1024 and sys.argv[2] > 1024 and sys.argv[3] > 1024 and sys.argv[4] > 1024):
        print("Invalid port numbers used.")
        sys.exit
    if not (sys.argv[1] < 64000 and sys.argv[2] < 64000 and sys.argv[3] < 64000 and sys.argv[4] < 64000):
            print("Invalid port numbers used.")
            sys.exit    
    
    #Create and bind all of the sockets
    
    if len(sys.argv) != 7:
        print("Too many command line arguments!")
        sys.exit
        
        

    channel_s_in = socket.socket(AF_INET, SOCKET.SOCK_STREAM)
    channel_s_in.bind(("", sys.argv[1]))
    
    channel_s_out = socket.socket(AF_INET, SOCKET.SOCK_STREAM)
    channel_s_out.bind(("", sys.argv[2]))

    channel_r_in = socket.socket(AF_INET, SOCKET.SOCK_STREAM)
    channel_r_in.bind(("", sys.argv[3]))
    
    channel_r_out = socket.socket(AF_INET, SOCKET.SOCK_STREAM)
    channel_r_out.bind(("", sys.argv[4]))
    
    
    s_in_port = ('localhost', sys.argv[5])
    r_in_port = ('localhost', sys.argv[6])
    
    packet_loss_rate = float(sys.argv[7])
   
    channel_s_out.connect((host, port))
    channel_r_out.connect((host, port))
    
    
    #Enters an infinite loop to perform tasks
    while 1:
        pass
    
    

    
class Packet(object, maginco, p_type, seqno, dataLen):
    def __init__(self):
        self.maginco = maginco
        self.p_type = p_type
        self.seqno = seqno
        self.dataLen = dataLen
        self.data = data

