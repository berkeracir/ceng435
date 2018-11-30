import socket
import sys
import datetime as dt

SOCKET_SIZE = 1024

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

broker_address = ('localhost', 10003)

try:
    sock.connect(broker_address)
except:
    print "Connection Error:", broker_address
    sys.exit()

try:

    while True:
        message = raw_input("Message: ")

        # Send data
        #sent = sock.sendto(message, broker_address)
        #print "\tSending:", message, "\n\t\tto (Broker):", broker_address, "(%i)" % sent
        sock.sendall(dt.datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f"))
        print "\tSending:", message, "(%d)" % sys.getsizeof(message), "\n\t\tto (Broker):", broker_address, "\n"

finally:
    sock.close()