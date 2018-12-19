import socket
import sys


# Initialize buffer size for socket
SOCKET_SIZE = 1024

# Create socket with UDP connection
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Check whether we get expected arguments.If we do not get, exit from script
# We need to get Router&Destination IP and Port number
# Note that we gave this arguments in our script which executes all nodes
if len(sys.argv) < 5:
    print "Expected Arguments:", sys.argv[0], "<ROUTER-IP>", "<ROUTER-PORT>", "<DESTINATION-IP>", "<DESTINATION-PORT>"
    sys.exit()

# Assign argv variables to router address and destination address
router_address = (sys.argv[1], int(sys.argv[2]))
destination_address = (sys.argv[3], int(sys.argv[4]))

# Bind the socket to address router address
# In case of exception, exit from script
try:
    sock.bind(router_address)

    # Get continous packets
    while True:
        # Receive data from UDP connection
        data, address = sock.recvfrom(SOCKET_SIZE)
        print "Message:", data, "\n\tfrom:", address
        # Send data to destination
        sent = sock.sendto(data, destination_address)
        print "\tto:", destination_address
except:
    sys.exit()
finally:
    sock.close()
