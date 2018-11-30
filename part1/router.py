import socket
import sys

SOCKET_SIZE = 5

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10001)
client_address = ('localhost', 10000)
try:
    sock.bind(server_address)
except:
    sys.exit()

while True:
    data, address = sock.recvfrom(SOCKET_SIZE) #buffersize
    sent = sock.sendto(data, client_address)