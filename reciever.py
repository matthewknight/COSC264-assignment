import socket
import sys
import packet

#Default port numbers to use : 38764 21983 x y

23501
def reciever():
    
    if len(sys.argv) != 5:
        print("ERROR:", len(sys.argv)-1, "argument(s) passed. Please make sure there are 4.")
        sys.exit(0)  
            
    if int(sys.argv[1]) < 1024 or int(sys.argv[2]) < 1024:
        print("Invalid port numbers used. Check numbers and try again.")
        sys.exit(0)  
    
    if int(sys.argv[1]) > 64000 or int(sys.argv[2]) > 64000:
        print("Invalid port numbers used. Check numbers and try again.")
        sys.exit(0) 
    print("Here")
    #Create/bind both sockets
    recieve_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recieve_in.bind(('', int(sys.argv[1])))
    recieve_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recieve_out.bind(('', int(sys.argv[2])))
    
    print('Connecting...')
    recieve_in.connect(('', 23501)) #sender socket_out
    print('Listening...')
    
    print('Connected by', addr)
    
    
reciever()