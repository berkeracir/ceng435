from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime
import sys

if len(sys.argv) < 2:
    sys.stderr.write(sys.argv[0] + " <file-to-be-sent>\n")

SOCKET_SIZE = 1024
MAX_HEADER_SIZE = len("5000||65535")

BROKER_IP = "10.10.1.2"
BROKER_PORT = 51795
BROKER = (BROKER_IP, BROKER_PORT)

tcp_sock = socket(AF_INET, SOCK_STREAM)
tcp_sock.connect(BROKER)

with open(sys.argv[1], "rb") as f:
    data = f.read(SOCKET_SIZE-MAX_HEADER_SIZE)
    tstart = datetime.now()
    
    while data:
        tcp_sock.send(data)
        rcv_data = tcp_sock.recv(SOCKET_SIZE)

        data = f.read(SOCKET_SIZE-MAX_HEADER_SIZE)

    tend = datetime.now()
    #delta = float((tend - tstart).seconds)*1000 + float((tend - tstart).microseconds/1000.0)
    delta = tend - tstart
    sys.stdout.write("File %s is sent in total of %f seconds.\n" % (sys.argv[1], delta.total_seconds()))
    print tend, tstart

tcp_sock.close()
sys.exit()