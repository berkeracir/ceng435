import socket
import sys
from random import randint


# Initialize buffer size for socket
SOCKET_SIZE = 1024

# Create socket with TCP to get data from source
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Create socket with UDP to send data routers
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# If we do not get expected arguments exit from script.
# Note that we gave this arguments in our script which executes all nodes
if len(sys.argv) < 7:
    print "Expected Arguments:", sys.argv[0], "<BROKER-IP>", "<BROKER-PORT>", "<ROUTER1-IP>", "<ROUTER1-PORT>", "<ROUTER2-IP>", "<ROUTER2-PORT>"
    sys.exit()

# Assign argv variables to broker and routers' address
broker_address = (sys.argv[1], int(sys.argv[2]))
router1_address = (sys.argv[3], int(sys.argv[4]))
router2_address = (sys.argv[5], int(sys.argv[6]))

# Bind the socket to address broker address
tcp_sock.bind(broker_address)

# Listen for connections made to the socket, for this case there is 1 listener
tcp_sock.listen(1)

while True:
     # Accept a connection
    (connection, address) = tcp_sock.accept()

    try:
        # Get continous TCP byte streams
        while True:
            # Receive data from TCP connection
            data = connection.recv(SOCKET_SIZE)
            print "Message:", data, "\n\tfrom:", address
            
            # As long as there is a data stay in while loop
            if data:
                # Get random number, if it is 1 send data to router-1 with UDP connection, else (random number is 0) send data to router-2 with UDP connection
                if randint(0,1):
                    udp_sock.sendto(data, router1_address)
                    print "\tto:", router1_address
                else:
                    udp_sock.sendto(data, router2_address)
                    print "\tto:", router2_address

            # If there is no data go to finally block
            else:
                break

    # After all done, close the connection 
    finally:
        connection.close()
