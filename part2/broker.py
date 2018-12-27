from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM, timeout
from datetime import datetime
import sys

if len(sys.argv) < 2:
    sys.stderr.write(sys.argv[0] + " <file-to-be-written-in>\n")

# Initialize socket, window and max header size
                                # -> max size of 'checksum' + '|' + 'sequence number' + '|'
SOCKET_SIZE = 1000
WINDOW_SIZE = 64
MAX_HEADER_SIZE = len("5000||65535")

# Initialize parameters to set timeout value
estimated_rtt = 100.0
dev_rtt = 0.0

# Calculate IPv4 Checksum for given data
def calculate_checksum(message):
    s = 0
    if len(message) % 2 == 0:
        for i in range(0, len(message), 2):
            w = ord(message[i]) + (ord(message[i+1]) << 8) 
            s = (s + w & 0xffff) + (s + w >> 16)
    else:
        for i in range(0, len(message)-1, 2):
            w = ord(message[i]) + (ord(message[i+1]) << 8) 
            s = (s + w & 0xffff) + (s + w >> 16)
        # TODO: update s one more time!
    return ~s & 0xffff

# Calculate Timeout value depending on previous RTT and its deviation
def calculate_timeout(sample_rtt):
    global estimated_rtt
    global dev_rtt

    alpha = 0.5
    beta = 0.125
    estimated_rtt = (1-alpha)*estimated_rtt + alpha*sample_rtt
    dev_rtt = (1-beta)*dev_rtt + beta*abs(sample_rtt-estimated_rtt)

# Packetize data with the given content and sequence number
def packetize(seq, content):
    msg = str(seq) + "|" + content + "|"
    msg_send = msg + str(calculate_checksum(msg))

    return msg_send

# Initialize broker address
BROKER_IP = "10.10.1.2"
BROKER_PORT = 51795
BROKER = (BROKER_IP, BROKER_PORT)

# TODO: add IP 10.10.3.2 too   #TODO COMMENNT
DEST_IP_1 = "10.10.5.2"
DEST_IP_2 = "10.10.5.2"
DEST_PORT = 51795
DEST_1 = (DEST_IP_1, DEST_PORT)
DEST_2 = (DEST_IP_2, DEST_PORT)

# Create sockets
send_sock = socket(AF_INET, SOCK_DGRAM) # udp socket to send data to destination
recv_sock = socket(AF_INET, SOCK_DGRAM) # udp socket to receive data from destination
tcp_sock = socket(AF_INET, SOCK_STREAM) # tcp socket to receive data from source

try:
    # TODO
    #Bind socket to broker and initialize first timeout value
    recv_sock.bind(("0.0.0.0", 51795))
    recv_sock.settimeout((estimated_rtt+4*dev_rtt)/1000.0)

    # Bind tcp socket
    tcp_sock.bind(BROKER)
    tcp_sock.listen(1)
    # Establish a connection
    connection, address = tcp_sock.accept()

    f = open(sys.argv[1], "w+")
    # initialize sequence number,base and msg_list
    seq = 0
    base = 0
    msg_list = [] # We use msg_list to store data which taken from source
                  # The reason why we use msg_list is to store data that we did not receives
                    # acks because we cannot take same data from source in our design
                  # Onces we receives acks, we pop data from list. If we don't, we keep data in list, and send it after iteration

    data_done = False
    while True: 
        # As long as data is not null, fill up the msg_list with the data that we receive
        if not data_done:
            # Exit from loop when msg_list's length is same with the window size
            while seq < base + WINDOW_SIZE:
                data = connection.recv(SOCKET_SIZE-MAX_HEADER_SIZE)
                # If data is not null, append it to msg_list
                if data:
                    f.write(data)
                    msg_list.append(data)
                    seq += 1
                else:
                    data_done = True
                    break

                connection.sendall(data)
        # Packetize all data in masg_list and send it to destination
        for index in range(len(msg_list)):
            # Start time after sending first packet
            if index == 0:
                tstart = datetime.now()
            # Set sequence number
            msg_seq = base + index
            # Send the same data over two link, we decreased probability of lossing data by this way.
            send_sock.sendto(packetize(msg_seq, msg_list[index]), DEST_1)
            send_sock.sendto(packetize(msg_seq, msg_list[index]), DEST_2)

        # Try to receive acks of data that we send
        ack_count = 0
        while ack_count < WINDOW_SIZE:
            try:
                # Receive ack data from destination
                message, address = recv_sock.recvfrom(SOCKET_SIZE)
            # In case of time out break, stop receiving acks
            except timeout:
                break
            except KeyboardInterrupt:
                raise
            else:
                # When we receive first ack, stop timer and calculate rtt
                # By using rtt set new timeout value
                if ack_count == 0:
                    tend = datetime.now()
                    delta = tend - tstart
                    rtt = float(float(delta.microseconds)/1000)
                    calculate_timeout(rtt)
                    recv_sock.settimeout((estimated_rtt+4*dev_rtt)/1000.0)

                try:
                    # Split the ack data, now we have checksum and sequence number of ack
                    checksum = message.split('|')[-1]
                    ack_seq = message.split('|')[0]
                # If we get corrupt ack message increase ack_count and continue from beginning of loop
                except ValueError:
                    ack_count += 1
                    continue
                # If sequence number and checksum are okey, pop the data from list which we received acks of
                if calculate_checksum(ack_seq + "|") == int(checksum) and int(ack_seq) >= base:
                    for i in range(int(ack_seq) - base + 1):
                        base += 1
                        msg_list.pop(0)

                        ack_count += 1
        
        if data_done and seq == base: # This means we send all data, close broker
            break
except:
    sys.stderr.write("Connection error or IDK\n")
finally:
    # Close connection
    f.close()
    connection.close()  