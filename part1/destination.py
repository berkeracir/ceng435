import socket
import sys
from thread import *
import datetime as dt

SOCKET_SIZE = 1024

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if len(sys.argv) < 3:
    print "Expected Arguments:", sys.argv[0], "<DESTINATION-IP>", "<DESTINATION-PORT>"
    sys.exit()

# Bind the socket to the port
destination_address = (sys.argv[1], int(sys.argv[2]))

try:
    sock.bind(destination_address)
except:
    print "Socket Binding Exception"
    sys.exit()

def clientThread(data, address, time):
    
    while True:
        msg_time = dt.datetime.strptime(data, "%Y/%m/%d %H:%M:%S.%f")
        time_diff = time - msg_time
        delay_in_ms = time_diff.days*24*60*60*1000 + time_diff.seconds*1000 + time_diff.microseconds/1000.0
        print "Received Message:", data, "\n\tfrom:", address, "\n\ttime diff:", delay_in_ms, "ms"
        data, address = sock.recvfrom(SOCKET_SIZE)
        time = dt.datetime.now()

while True:
    #buffersize
    data, address = sock.recvfrom(SOCKET_SIZE)
    time = dt.datetime.now()
    if data:
        start_new_thread(clientThread, (data, address, time, ))