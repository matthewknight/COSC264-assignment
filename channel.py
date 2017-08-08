import socket
import sys
import packet
  
  
# 7 Test Port Numbers for ctrl-c :  38001 43874 23524 2569 7839 8432 0.1  

def channel():
    """Takes 7 command line arguments. These are:
       -Four port numbers csin, csout, crin, crout
       -One port number sin socket of sender (To which channel will send packets to sender
       -One port number rin socket of the reciever (To which channel will send packets to reciever.
       -A floating point P which is the Packet Loss Rate. 0 <= P < 1
    """
     
    #Check if all arguments were recieved
    if len(sys.argv) != 8:
        print("ERROR:", len(sys.argv), "argument(s) passed. Please make sure there are 7.")
        sys.exit(0)
    #Check if all port numbers are valid. 1024 <= port < 64000

    if int(sys.argv[1]) < 1024 or int(sys.argv[2]) < 1024 or int(sys.argv[3]) < 1024 or int(sys.argv[4]) < 1024:
        print("Invalid port numbers used. Check numbers and try again.")
        sys.exit(0)
    
    if int(sys.argv[1]) > 64000 or int(sys.argv[2]) > 64000 or int(sys.argv[3]) > 64000 or int(sys.argv[4]) > 64000:
        print("Invalid port numbers used. Check numbers and try again.2") 
        sys.exit(0)   
    
    if float(sys.argv[7]) < 0.0 or float(sys.argv[7]) > 1.0:
        print("Precision value out of range!")
        sys.exit(0)
        
        
    
    #Create and bind all of the sockets
         

    channel_s_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    channel_s_in.bind(('', int(sys.argv[1])))
    
    channel_s_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    channel_s_out.bind(('', int(sys.argv[2])))

    channel_r_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    channel_r_in.bind(('', int(sys.argv[3])))
    
    channel_r_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    channel_r_out.bind(('', int(sys.argv[4])))
    
    
    s_in_port = ('localhost', int(sys.argv[5]))
    r_in_port = ('localhost', int(sys.argv[6]))
    
    packet_loss_rate = float(sys.argv[7])
   
   
   
   
   
    print('Connecting...')
    
    try:
        channel_s_out.connect(('', 7642))
        channel_r_out.connect(('', 38764))
    except socket.error as socketerror:
            print("Error: ", socketerror)  
            sys.exit(0)
    
    
    #Enters an infinite loop to perform tasks
    while 1:
        print("yaa")

channel() 