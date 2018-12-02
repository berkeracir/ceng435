import socket
import sys
import thread
import datetime as dt
from time import sleep

SOCKET_SIZE = 1024
if len(sys.argv) < 5:
    print "Expected Arguments:", sys.argv[0], "<DESTINATION1-IP>", "<DESTINATION1-PORT>", "<DESTINATION2-IP>", "<DESTINATION2-PORT>"
    sys.exit()

# Bind the socket to the port
destination1_address = (sys.argv[1], int(sys.argv[2]))
destination2_address = (sys.argv[3], int(sys.argv[4]))

total_delay = 0.0
count = 0

def clientThread(data, address, time):
    global total_delay
    msg_time = dt.datetime.strptime(data.split('|')[1], "%Y/%m/%d %H:%M:%S.%f")
    time_diff = time - msg_time
    delay_in_ms = time_diff.days*24*60*60*1000 + time_diff.seconds*1000 + time_diff.microseconds/1000.0
    total_delay += delay_in_ms
    print "Received Message:", data.split('|')[0], "at:", time.strftime("%Y/%m/%d %H:%M:%S.%f"), "\n\tfrom:", address, "\n\ttime diff:", delay_in_ms, "ms"
    #time = dt.datetime.now()

def serverThread(address):
    # Create a UDP socket
    global count
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.bind(address)

        while True:
            data, address = sock.recvfrom(SOCKET_SIZE)
            time = dt.datetime.utcnow()

            if data:

                count += 1
                thread.start_new_thread(clientThread, (data, address, time, ))
    except:
        print "Socket Binding Exception:", address
        sys.exit()
    

thread.start_new_thread(serverThread, (destination1_address, ))
thread.start_new_thread(serverThread, (destination2_address, ))

while True:
    try:
        avg = total_delay/count
    except ZeroDivisionError:
        avg = 0
    
    print "Average Delay:", avg, "ms (" + str(total_delay) + " ms/" + str(count) + ")"
    sleep(10)
