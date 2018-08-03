import socket

HOST = '10.100.15.212'  # Standard loopback interface address (localhost)
PORT = 3100        # Port to listen on (non-privileged ports are > 1023)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

while True:
    data, addr = server_socket.recvfrom(1024)
    print('Connected by', addr)
    print("recevied message: ", data)

    if data == b'\x8f\x8f\x8f\x8f\xaa\xbb\xcc\xdd\xee\xff\x00\x00\x00\x00\x06\x00\xff':
        server_socket.sendto(b'\x8f\x8f\x8f\x8f\xAA\xbb\xcc\xdd\xee\xff\x01\x00\x00\x00\x06\x01\x01\xff', addr)
