import socket
import sys

SOCKET_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if len(sys.argv) < 5:
    print "Expected Arguments:", sys.argv[0], "<ROUTER-IP>", "<ROUTER-PORT>", "<DESTINATION-IP>", "<DESTINATION-PORT>"
    sys.exit()

router_address = (sys.argv[1], int(sys.argv[2]))
destination_address = (sys.argv[3], int(sys.argv[4]))

try:
    sock.bind(router_address)
except:
    sys.exit()

while True:
    data, address = sock.recvfrom(SOCKET_SIZE)
    print "Message:", data, "\n\tfrom:", address
    sent = sock.sendto(data, destination_address)
    print "\tto:", destination_address
