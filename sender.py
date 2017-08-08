import socket

def server_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 42169
    
    s.bind((host, port))
    
    message = "You lika deez nutz?"
    b = bytearray()
    b.extend(message.encode())
    
    
    s.listen(5)
    while True:
        c, addr = s.accept()
        print('Got connection from {}'.format(addr))
        c.send(b)
        c.close()
        
server_socket()