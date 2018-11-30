import socket
import sys

# Create a UDP socket TODO: make it TCP!
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10001)
while True:
    message = raw_input("Message: ")

    try:
        # Send data
        sent = sock.sendto(message, server_address)
        print "\tSending:", message, "\n\t\tto:", server_address, "(%i)" % sent

    except:
        sock.close()
        print "Closing the socket"