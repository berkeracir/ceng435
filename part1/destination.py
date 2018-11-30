import socket
import sys
from thread import *

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('', 10000)

try:
    sock.bind(server_address)
except:
    sys.exit()

def clientThread(data):
    while 1:
        print >>sys.stderr, data
        
        '''if data:
            sent = sock.sendto(data, address)
            print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)'''
        data, address = sock.recvfrom(1024) 




while True:
    #buffersize
    data, address = sock.recvfrom(1024) 
    if data:
        start_new_thread(clientThread, (data, ))
    
    

