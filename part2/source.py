from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime
import sys

if len(sys.argv) < 2:
    sys.stderr.write(sys.argv[0] + " <file-to-be-sent>\n")

# Initialize socket, window and max header size
# max size of 'checksum' + '|' + 'sequence number' + '|'
SOCKET_SIZE = 1000
MAX_HEADER_SIZE = len("5000||65535")

# Set Broker address
BROKER_IP = "10.10.1.2"
BROKER_PORT = 51795
BROKER = (BROKER_IP, BROKER_PORT)

# Create TCP socket and connect to Broker
tcp_sock = socket(AF_INET, SOCK_STREAM)
tcp_sock.connect(BROKER)

# Open the input file which will be transmitted
with open(sys.argv[1], "rb") as f:
    data = f.read(SOCKET_SIZE-MAX_HEADER_SIZE)
    tstart = datetime.now()
    
    # Get all data from file, send it to the broker
    while data:
        tcp_sock.send(data)
        rcv_data = tcp_sock.recv(SOCKET_SIZE)

        data = f.read(SOCKET_SIZE-MAX_HEADER_SIZE)

    # Calculate the time between before sending first 
    # data and after receiving last ack, print it
    tend = datetime.now()
    delta = tend - tstart
    sys.stdout.write("%f seconds\n" % (delta.total_seconds()))

# Close the socket
tcp_sock.close()
sys.exit()