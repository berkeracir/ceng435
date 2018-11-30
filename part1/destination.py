import socket
import sys
from thread import *
import datetime as dt

SOCKET_SIZE = 1024

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)

try:
    sock.bind(server_address)
except:
    print "Socket Binding Exception"
    sys.exit()

def clientThread(data, address, time):
    
    while True:
        msg_time = dt.datetime.strptime(data, "%Y/%m/%d %H:%M:%S.%f")
        time_diff = time - msg_time
        print "Received Message:", data, "\n\tfrom:", address, "\n\ttime diff:", time_diff.days*24*60*60*1000 + time_diff.seconds*1000 + time_diff.microseconds, "ms"
        data, address = sock.recvfrom(SOCKET_SIZE)
        time = dt.datetime.now()

while True:
    #buffersize
    data, address = sock.recvfrom(SOCKET_SIZE)
    time = dt.datetime.now()
    if data:
        start_new_thread(clientThread, (data, address, time, ))