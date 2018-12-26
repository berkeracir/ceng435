from socket import socket, AF_INET, SOCK_DGRAM, timeout
import sys

if len(sys.argv) < 2:
    sys.stderr.write(sys.argv[0] + " <file-to-be-written-in>\n")

SOCKET_SIZE = 1024

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

send_sock = socket(AF_INET, SOCK_DGRAM)
recv_sock = socket(AF_INET, SOCK_DGRAM)

exp_seq = 0

try:
    dest_timeout = 15
    recv_sock.bind(DEST)
    recv_sock.settimeout(dest_timeout)

    f = open(sys.argv[1], "w+")

    while True:
        # Received message must be in the format of seq|message|checksum
        message, address = recv_sock.recvfrom(SOCKET_SIZE)

        # Try Except block is for detecting corrupted message delimiter('|')
        try:
            checksum = message.split('|')[-1]
            data = "|".join(message.split('|')[:-1]) + "|"
            ack_seq = data.split('|')[0]
            content = "|".join(data.split('|')[1:-1])

            #print "Received:", ack_seq
        except ValueError:
            print "Corrupted ACK Message"
            # TODO send NACK in case of receiving corrupted message
            continue

        #print message

        # Receiving message with expected sequence number equal to sequence number
        if calculate_checksum(data) == int(checksum) and str(exp_seq) == ack_seq:
            f.write(content)
            #print "Writing:", ack_seq
            
            ack_msg = ack_seq + "|"
            msg_send = ack_msg + str(calculate_checksum(ack_msg))
            send_sock.sendto(msg_send, BROKER)
            exp_seq += 1

            print "ACK:", ack_seq
        # Receiving message with expected sequence number greater than sequence number
        # That means BROKER didn't received my previous ACK message
        #elif calculate_checksum(data) == int(checksum) and exp_seq > int(ack_seq):
            #ack_msg = ack_seq + "|"
            #msg_send = ack_msg + str(calculate_checksum(ack_msg))
            #send_sock.sendto(msg_send, BROKER)

            #print "Re-sending:", ack_seq
        # TODO send NACK in case of receiving corrupted message
        else:
            ack_msg = str(exp_seq-1) + "|"
            msg_send = ack_msg + str(calculate_checksum(ack_msg))
            send_sock.sendto(msg_send, BROKER)

            print "rACK:", exp_seq-1, "(" + ack_seq + ")"

except timeout:
    f.close()
    sys.stderr.write("%s is closed after waiting %d seconds.\n" % (sys.argv[0], dest_timeout))
    sys.exit()
