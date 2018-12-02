import socket
import sys
import datetime as dt
from time import sleep

# Initilaze buffer size for socket
SOCKET_SIZE = 1024

# Create socket with TCP connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Check whether we get expected arguments.If we do not get, exit from script
# We need to get broker IP and port number
# Note that we gave this arguments in our script which executes all nodes  
if len(sys.argv) < 3:
    print "Expected Arguments:", sys.argv[0], "<BROKER-IP>", "<BROKER-PORT>"
    sys.exit()

# Assign argv variables to broker address
broker_address = (sys.argv[1], int(sys.argv[2]))

# Try-except block for connection socket to broker address 
# In case of exception, exit from script
try:
    sock.connect(broker_address)

    for i in range(0,1000):
        message = str(i)    # = raw_input("Message: ") //alternative
        # Get the current time 
        date_msg = dt.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S.%f")
        #  Send data to broker
        sock.sendall(message + "|" + date_msg)
        print "\tSending:", message, "(%d)" % sys.getsizeof(message), "\n\t\tto (Broker):", broker_address, "\n"

        sleep(0.03)
except:
    print "Connection Error:", broker_address
    sys.exit()
# After all done close socket and exit from script
finally:
    sock.close()
