import socket
import sys
from random import randint

SOCKET_SIZE = 1024

# Create a TCP/IP socket
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if len(sys.argv) < 7:
    print "Expected Arguments:", sys.argv[0], "<BROKER-IP>", "<BROKER-PORT>", "<ROUTER1-IP>", "<ROUTER1-PORT>", "<ROUTER2-IP>", "<ROUTER2-PORT>"
    sys.exit()

broker_address = (sys.argv[1], int(sys.argv[2]))
router1_address = (sys.argv[3], int(sys.argv[4]))
router2_address = (sys.argv[5], int(sys.argv[6]))

tcp_sock.bind(broker_address)
tcp_sock.listen(1)

while True:
    (connection, address) = tcp_sock.accept()

    try:
        while True:
            data = connection.recv(SOCKET_SIZE)
            print "Message:", data, "\n\tfrom:", address
            
            if data:
                if randint(0,1):
                    udp_sock.sendto(data, router1_address)
                    print "\tto:", router1_address
                else:
                    udp_sock.sendto(data, router2_address)
                    print "\tto:", router2_address

            else:
                break

    finally:
        connection.close()