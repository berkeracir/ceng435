import socket
import sys
import datetime as dt

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
    while True:
        message = raw_input("Message: ")

        # Send data
        sock.sendall(dt.datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f"))
        print "\tSending:", message, "(%d)" % sys.getsizeof(message), "\n\t\tto (Broker):", broker_address, "\n"

finally:
    sock.close()