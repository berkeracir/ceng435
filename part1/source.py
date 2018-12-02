import socket
import sys
import datetime as dt
from time import sleep

SOCKET_SIZE = 1024

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) < 3:
    print "Expected Arguments:", sys.argv[0], "<BROKER-IP>", "<BROKER-PORT>"
    sys.exit()

broker_address = (sys.argv[1], int(sys.argv[2]))

try:
    sock.connect(broker_address)
except:
    print "Connection Error:", broker_address
    sys.exit()

try:
    #while True:
    for i in range(0,1000):
        #message = raw_input("Message: ")
        message = str(i)
        date_msg = dt.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S.%f")

        # Send data
        sock.sendall(message + "|" + date_msg)
        print "\tSending:", message, "(%d)" % sys.getsizeof(message), "\n\t\tto (Broker):", broker_address, "\n"

        sleep(0.03)

finally:
    sock.close()
