import socket
import sys

SOCKET_SIZE = 5

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
        sock.sendall(message)
        print "\tSending:", message, "\n\t\tto (Broker):", broker_address
        
        # Look for the response
        """amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = sock.recv(SOCKET_SIZE)
            amount_received += len(data)
            print "\nreceived:", data"""

finally:
    sock.close()