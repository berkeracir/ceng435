from socket import socket, AF_INET, SOCK_DGRAM, timeout
import sys

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

SOURCE_IP = "localhost"
SOURCE_PORT = 9999
SOURCE = (SOURCE_IP, SOURCE_PORT)

BROKER_IP = "localhost"
BROKER_PORT = 10000
BROKER = (BROKER_IP, BROKER_PORT)

DEST_IP = "localhost"
DEST_PORT = 10001
DEST = (DEST_IP, DEST_PORT)

SOCKET_SIZE = 1024

send_sock = socket(AF_INET, SOCK_DGRAM)
recv_sock = socket(AF_INET, SOCK_DGRAM)

recv_sock.bind(DEST)

exp_seq = 0
a = open("serverdata.txt", "w+")
while True:
    # Received message must be in the format of seq|message|checksum
    message, address = recv_sock.recvfrom(SOCKET_SIZE)

    # Try Except block is for detecting corrupted message delimiter('|')
    try:
        checksum = message.split('|')[-1]
        data = "|".join(message.split('|')[:-1]) + "|"
        ack_seq = data.split('|')[0]
        content = "|".join(data.split('|')[1:-1])
    except ValueError:
        "Corrupted ACK Message"
        ack_msg = str(exp_seq - 1) + "|"
        msg_send = ack_msg + str(calculate_checksum(ack_msg))
        send_sock.sendto(msg_send, BROKER) 

    #print message

    # Receiving message with expected sequence number equal to sequence number
    if calculate_checksum(data) == int(checksum) and str(exp_seq) == ack_seq:
        print "seqnum :    " + ack_seq
        
        ack_msg = ack_seq + "|"
        msg_send = ack_msg + str(calculate_checksum(ack_msg))
        send_sock.sendto(msg_send, BROKER)
        exp_seq += 1
        a.write(content)
    # Receiving message with expected sequence number greater than sequence number
    # That means BROKER didn't received my previous ACK message
    else:
        ack_msg = str(exp_seq - 1) + "|"
        msg_send = ack_msg + str(calculate_checksum(ack_msg))
        send_sock.sendto(msg_send, BROKER) 
    # else: TODO send NACK in case of receiving corrupted message
