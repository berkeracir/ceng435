import socket
import sys
import thread
import datetime as dt

SOCKET_SIZE = 1024

# Create a UDP socket
sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if len(sys.argv) < 5:
    print "Expected Arguments:", sys.argv[0], "<DESTINATION1-IP>", "<DESTINATION1-PORT>", "<DESTINATION2-IP>", "<DESTINATION2-PORT>"
    sys.exit()

# Bind the socket to the port
destination1_address = (sys.argv[1], int(sys.argv[2]))
destination2_address = (sys.argv[3], int(sys.argv[4]))

def clientThread(data, address, time):
    msg_time = dt.datetime.strptime(data.split('|')[1], "%Y/%m/%d %H:%M:%S.%f")
    time_diff = time - msg_time
    delay_in_ms = time_diff.days*24*60*60*1000 + time_diff.seconds*1000 + time_diff.microseconds/1000.0
    print "Received Message:", data.split('|')[0], "\n\tfrom:", address, "\n\ttime diff:", delay_in_ms, "ms"
    time = dt.datetime.now()

def serverThread(address):
    try:
        sock.bind(address)
    except:
        print "Socket Binding Exception:", address
        sys.exit()

    while True:
        data, address = sock.recvfrom(SOCKET_SIZE)

        if data:
            time = dt.datetime.now()
            thread.start_new_thread(clientThread, (data, address, time, ))

thread.start_new_thread(serverThread, (destination1_address, ))
thread.start_new_thread(serverThread, (destination2_address, ))

