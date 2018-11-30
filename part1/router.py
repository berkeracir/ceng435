import socket
import sys

SOCKET_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if len(sys.argv) < 2:
    sys.exit()

router1_address = ('localhost', int(sys.argv[1]))
destination_address = ('localhost', 10000)

try:
    sock.bind(router1_address)
except:
    sys.exit()

while True:
    data, address = sock.recvfrom(SOCKET_SIZE) #buffersize
    sent = sock.sendto(data, destination_address)