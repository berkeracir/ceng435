import socket
import sys

SOCKET_SIZE = 5

# Create a TCP/IP socket
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

source_address = ('localhost', 10003)
router1_address = ('localhost', 10001)

tcp_sock.bind(source_address)
tcp_sock.listen(1)

while True:
    (connection, address) = tcp_sock.accept()

    try:
        while True:
            data = connection.recv(SOCKET_SIZE)

            if data:
                print "Received message:", data, "\n\tfrom (Source):", address
                udp_sock.sendto(data, router1_address)
                print "Sending message:", data, "\n\tto (Router-1):", router1_address

            else:
                break


    finally:
        connection.close()