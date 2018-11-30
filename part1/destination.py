import socket
import sys
from thread import *

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)

try:
    sock.bind(server_address)
except:
    print "Socket Binding Exception"
    sys.exit()

def clientThread(data, address):
    
    while True:
        print "Received Message:", data, "\n\tfrom:", address
        data, address = sock.recvfrom(1024)

while True:
    #buffersize
    data, address = sock.recvfrom(1024) 
    if data:
        start_new_thread(clientThread, (data, address, ))