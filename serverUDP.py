import socket
import sys
from thread import *

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
try:
    sock.bind(server_address)
except:
    sys.exit()

def clientThread(data):
 
    print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
    print >>sys.stderr, data
    
    if data:
        sent = sock.sendto(data, address)
        print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)




while True:
    data, address = sock.recvfrom(1024) #buffersize
    start_new_thread(clientThread, (data, ))
