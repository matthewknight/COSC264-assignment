import socket

#Client
def sender_socket(s_IN_Port=42070, s_OUT_Port=42071, c_IN_Port=42069, filename=None):
    host = socket.gethostname()
    
    s_IN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_IN.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_IN.bind((host, s_IN_Port))
    
    s_OUT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_OUT.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_OUT.bind((host, s_OUT_Port))
    
    #c_IN_Port represents destination, in this case receiver
    s_OUT.connect((host, c_IN_Port))
    
    print("Initialised")
    
    messageToSend = b"You lika deez nutz?"
    print("Sent", repr(messageToSend))
    s_OUT.send(messageToSend)
    
    s_IN.listen(1)
    
    data = s_IN.recv(1024)
    s_IN.close()
    print("Received", repr(data))

    
def main(): 
    sender_socket()
    
main()