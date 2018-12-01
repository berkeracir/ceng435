import socket
import sys

SOCKET_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if len(sys.argv) < 3:
    print "Expected Arguments:", sys.argv[0], "<ROUTER-IP>", "<ROUTER-PORT>"
    sys.exit()

router_address = (sys.argv[1], int(sys.argv[2]))
destination_address = ('localhost', 10000)

try:
    sock.bind(router_address)
except:
    sys.exit()

while True:
    data, address = sock.recvfrom(SOCKET_SIZE)
    sent = sock.sendto(data, destination_address)