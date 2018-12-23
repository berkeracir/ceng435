from socket import socket, AF_INET, SOCK_STREAM
import sys

SOCKET_SIZE = 1024

SOURCE_IP = "localhost"
SOURCE_PORT = 9999
SOURCE = (SOURCE_IP, SOURCE_PORT)

BROKER_IP = "localhost"
BROKER_PORT = 10000
BROKER = (BROKER_IP, BROKER_PORT)

DEST_IP = "localhost"
DEST_PORT = 10001
DEST = (DEST_IP, DEST_PORT)

tcp_sock = socket(AF_INET, SOCK_STREAM)

try:
    tcp_sock.connect(SOURCE)

    with open(sys.argv[1], "rb") as f:
        data = f.read(SOCKET_SIZE)

        while data:
            tcp_sock.send(data)
            rcv_data = tcp_sock.recv(SOCKET_SIZE)

            data = f.read(SOCKET_SIZE)

except:
    print "Connection error"
    sys.exit()
finally:
    tcp_sock.close()