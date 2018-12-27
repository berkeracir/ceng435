from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime
import sys

if len(sys.argv) < 2:
    sys.stderr.write(sys.argv[0] + " <file-to-be-sent>\n")

# Initialize socket and max header size 
                        # -> max size of 'checksum' + '|' + 'sequence number' + '|'
SOCKET_SIZE = 1000
MAX_HEADER_SIZE = len("5000||65535")

# Set broker address
BROKER_IP = "10.10.1.2"
BROKER_PORT = 51795
BROKER = (BROKER_IP, BROKER_PORT)

# Create tcp socket and connect to broker
tcp_sock = socket(AF_INET, SOCK_STREAM)
tcp_sock.connect(BROKER)

# Open the file
with open(sys.argv[1], "rb") as f:
    data = f.read(SOCKET_SIZE-MAX_HEADER_SIZE)
    tstart = datetime.now()
    # Get all data from file, send it to the broker
    while data:
        tcp_sock.send(data)
        rcv_data = tcp_sock.recv(SOCKET_SIZE)

        data = f.read(SOCKET_SIZE-MAX_HEADER_SIZE)

    # Calculate the time between before sending first data and after receiving last ack, print it
    tend = datetime.now()
    delta = tend - tstart
    sys.stdout.write("%f seconds\n" % (delta.total_seconds()))

#close socket
tcp_sock.close()
sys.exit()