from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM, timeout
from datetime import datetime
import sys

if len(sys.argv) < 2:
    sys.stderr.write(sys.argv[0] + " <file-to-be-written-in>\n")

SOCKET_SIZE = 1024
WINDOW_SIZE = 1
MAX_HEADER_SIZE = len("5000||65535")

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

# Reliable Data Send over UDP connection
"""def rdt_send(seq, content, DEST):
    msg = str(seq) + "|" + content + "|"
    msg_send = msg + str(calculate_checksum(msg))

    tstart = datetime.now()
    send_sock.sendto(msg_send, DEST)

    # TODO: implement Go-Back-N method
    ack_received = False
    while not ack_received:
        try:
            message, address = recv_sock.recvfrom(SOCKET_SIZE)
            tend = datetime.now()
        except timeout: # In case of timeout, send the message again
            tstart = datetime.now()
            send_sock.sendto(msg_send, DEST)
        except KeyboardInterrupt:
            raise
        else:
            delta = tend - tstart
            rtt = float(float(delta.microseconds)/1000)

            # Try Except block is for detecting corrupted message delimiter('|')
            try:
                checksum = message.split('|')[-1]
                ack_seq = message.split('|')[0]
            except ValueError:
                # Corrupted ACK Message, send the previous message again
                continue

            if calculate_checksum(ack_seq + "|") == int(checksum) and ack_seq == str(seq):
                ack_received = True
                    
                calculate_timeout(rtt)
                recv_sock.settimeout((estimated_rtt+4*dev_rtt)/1000.0)

#def rdt_receive(seq)"""

def packetize(seq, content):
    msg = str(seq) + "|" + content + "|"
    msg_send = msg + str(calculate_checksum(msg))

    return msg_send

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
tcp_sock = socket(AF_INET, SOCK_STREAM)

try:
    recv_sock.bind(BROKER)
    recv_sock.settimeout((estimated_rtt+4*dev_rtt)/1000.0)

    tcp_sock.bind(SOURCE)
    tcp_sock.listen(1)

    connection, address = tcp_sock.accept()

    f = open(sys.argv[1], "w+")

    seq = 0
    base = 0
    msg_list = []

    data_done = False
    while True: # TODO: Implement Go-Back-N
        if not data_done:
            while seq < base + WINDOW_SIZE:
                data = connection.recv(SOCKET_SIZE-MAX_HEADER_SIZE)

                if data:
                    f.write(data)
                    msg_list.append(data)
                    seq += 1
                else:
                    data_done = True
                    break

                connection.sendall(data)

        for index in range(len(msg_list)):
            if index == 0:
                tstart = datetime.now()

            msg_seq = base + index
            send_sock.sendto(packetize(msg_seq, msg_list[index]), DEST)
            print "Sending:", msg_seq

        ack_count = 0
        while ack_count < WINDOW_SIZE:
            try:
                message, address = recv_sock.recvfrom(SOCKET_SIZE)
            except timeout:
                break
            except KeyboardInterrupt:
                raise
            else:
                if ack_count == 0:
                    tend = datetime.now()
                    delta = tend - tstart
                    rtt = float(float(delta.microseconds)/1000)
                    calculate_timeout(rtt)
                    recv_sock.settimeout((estimated_rtt+4*dev_rtt)/1000.0)

                ack_count += 1

                try:
                    checksum = message.split('|')[-1]
                    ack_seq = message.split('|')[0]

                    print "Received:", ack_seq, "base:" , base, "seq:", seq
                except ValueError:
                    print "Corrupted ACK Message" #, send the previous message again"
                    continue

                if calculate_checksum(ack_seq + "|") == int(checksum) and int(ack_seq) >= base:
                    for i in range(int(ack_seq) - base + 1):
                        base += 1
                        msg_list.pop()
        
        if data_done and seq == base:
            break
except:
    sys.stderr.write("Connection error or IDK\n")
finally:
    f.close()
    connection.close()