from socket import socket, AF_INET, SOCK_DGRAM, timeout
from datetime import datetime

SOCKET_SIZE = 1024

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

    alpha = 0.25
    beta = 0.25
    estimated_rtt = (1-alpha)*estimated_rtt + alpha*sample_rtt
    dev_rtt = (1-beta)*dev_rtt + beta*abs(sample_rtt-estimated_rtt)

SOURCE_IP = "localhost"
SOURCE_PORT = 10000
SOURCE = (SOURCE_IP, SOURCE_PORT)

DEST_IP = "localhost"
DEST_PORT = 10001
DEST = (DEST_IP, DEST_PORT)

send_sock = socket(AF_INET, SOCK_DGRAM)
recv_sock = socket(AF_INET, SOCK_DGRAM)

recv_sock.bind(SOURCE)
recv_sock.settimeout((estimated_rtt+4*dev_rtt)/1000.0)

seq = 0

while True:
    # TODO: get the data from 5 MB file and put it into a message
    user_input = raw_input("Message: ")

    msg = str(seq) + "|" + user_input + "|"
    msg_send = msg + str(calculate_checksum(msg))
    tstart = datetime.now()
    # Sending message in the format of seq|message|checksum
    # Checksum is calculated for seq|message|
    send_sock.sendto(msg_send, DEST)
    print "Sending:", msg_send, "(Timeout: " + str(recv_sock.gettimeout()*1000) + " ms)"

    # TODO: implement Go-Back-N method
    ack_received = False
    while not ack_received:
        try:
            message, address = recv_sock.recvfrom(SOCKET_SIZE)
            tend = datetime.now()
        except timeout: # In case of timeout, send the message again
            print "Timeout"
            tstart = datetime.now()
            send_sock.sendto(msg_send, DEST)
        except KeyboardInterrupt:
            raise
        else:
            delta = tend - tstart
            rtt = float(float(delta.microseconds)/1000)
            print "ACK message:", message, "(%f ms)" % rtt

            # Try Except block is for detecting corrupted message delimiter('|')
            try:
                checksum = message.split('|')[-1]
                ack_seq = message.split('|')[0]
            except ValueError:
                "Corrupted ACK Message"
                # Send the previous message again
                continue

            if calculate_checksum(ack_seq + "|") == int(checksum) and ack_seq == str(seq):
                ack_received = True
                    
                calculate_timeout(rtt)
                recv_sock.settimeout((estimated_rtt+4*dev_rtt)/1000.0)
                

    seq = seq + 1

