from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime
import sys

if len(sys.argv) < 2:
    sys.stderr.write(sys.argv[0] + " <file-to-be-sent>\n")

SOCKET_SIZE = 1024
MAX_HEADER_SIZE = len("5000||65535")

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
    tstart = datetime.now()

    with open(sys.argv[1], "rb") as f:
        data = f.read(SOCKET_SIZE-MAX_HEADER_SIZE)
        

        while data:
            tcp_sock.send(data)
            rcv_data = tcp_sock.recv(SOCKET_SIZE)

            data = f.read(SOCKET_SIZE-MAX_HEADER_SIZE)

    tend = datetime.now()
    delta = float((tstart - tend).microseconds)/1000.0
    sys.stdout.write("File %s is sent in total of %f ms.\n" % (sys.argv[1], delta))
finally:
    tcp_sock.close()
    sys.exit()