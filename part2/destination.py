from socket import socket, AF_INET, SOCK_DGRAM, timeout
import sys

if len(sys.argv) < 2:
    sys.stderr.write(sys.argv[0] + " <file-to-be-written-in>\n")

# Socket size
SOCKET_SIZE = 1000

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

# Set broker addresses
BROKER_IP_1 = "10.10.2.1"
BROKER_IP_2 = "10.10.4.1"
BROKER_PORT = 51795
BROKER_1 = (BROKER_IP_1, BROKER_PORT)
BROKER_2 = (BROKER_IP_2, BROKER_PORT)

# Open 2 UDP socket, one for receiving the data one for sending ACK messages
send_sock = socket(AF_INET, SOCK_DGRAM)
recv_sock = socket(AF_INET, SOCK_DGRAM)

exp_seq = 0

try:
     # Set destination timeout to 60 seconds, we close the 
     # destination socket after 60 seconds receiving last packet
    dest_timeout = 60
    recv_sock.bind(("0.0.0.0", 51795))
    recv_sock.settimeout(dest_timeout)

    f = open(sys.argv[1], "w+")

    while True:
        # Received message must be in the format of seq|message|checksum
        message, address = recv_sock.recvfrom(SOCKET_SIZE)

        # Try Except block is for detecting corrupted message delimiter('|')
        try:
            # Split message, get checksum, ack sequence number and data
            checksum = message.split('|')[-1]
            data = "|".join(message.split('|')[:-1]) + "|"
            ack_seq = data.split('|')[0]
            content = "|".join(data.split('|')[1:-1])
        except ValueError:
            print "Corrupted ACK Message"
            continue

        # Receiving message with expected sequence number equal to sequence number
        if calculate_checksum(data) == int(checksum) and str(exp_seq) == ack_seq:
            f.write(content)

            # Prepare ACK message -> ack_seq|checksum
            ack_msg = ack_seq + "|"
            msg_send = ack_msg + str(calculate_checksum(ack_msg))

            # Send ACK messages to Broker's addresses
            send_sock.sendto(msg_send, BROKER_1)
            send_sock.sendto(msg_send, BROKER_2)
            exp_seq += 1
        # Receiving message with expected sequence number greater than sequence number
        # That means BROKER didn't received my previous ACK message
        else:
            ack_msg = str(exp_seq-1) + "|"
            msg_send = ack_msg + str(calculate_checksum(ack_msg))
            
            # Send ACK messages to Broker's addresses
            send_sock.sendto(msg_send, BROKER_1)
            send_sock.sendto(msg_send, BROKER_2)
except timeout:
    # After timeout expires, close the server
    f.close()
    sys.stderr.write("%s is closed after waiting %d seconds.\n" % (sys.argv[0], dest_timeout))
    sys.exit()