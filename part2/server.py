import socket
import sys
from time import sleep

 ###### ###### ###### ###### ######  helper functions START ###### ###### ###### ###### ###### ###### ###### 

def calculate_checksum(message):
    s = 0
    for i in range(0, len(message), 2):
        w = ord(message[i]) + (ord(message[i+1]) << 8) 
        s = (s + w & 0xffff) + (s + w >> 16)
    return ~s & 0xffff

# Extracts sequence number, ack data and checksum from a non-empty packet
def extract_packet(packet):
    split1 = packet.find('|||')
    seq_num = int(packet[:split1])  #convert to int
    split2 = packet.find(' | ')
    checksum = int(packet[split2 + 3:]) #convert to int
    return seq_num, packet[split1 + 3:split2], checksum 

 ###### ###### ###### ###### ######  helper functions END ###### ###### ###### ###### ###### ###### ###### 

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = ('localhost', 10000)
sock.bind(server_address)

expected_seqnum = 0
i = 0

a= open("serverdata.txt","w+")
while True:
    try:
        
        #get packet
        packet, address = sock.recvfrom(1000)
        if not packet:
            continue

        #extract packet
        seq_num, data, checksum = extract_packet(packet)     
        print "seqnum:  " + str(seq_num)
        print "expectedseqnum:  " + str(expected_seqnum) 
        #it means we get null message, close server
        if checksum == 0 and seq_num == 0 and isinstance(checksum, int) :
            print "Client closed the socket"
            break
        #Check the data (sequence number, checksum)
        if seq_num == expected_seqnum and checksum == calculate_checksum(data):
            ack_packet = str(seq_num) + '|' + 'acknowledgement'
            sent = sock.sendto(ack_packet, address)
            expected_seqnum += 1
            print data
            a.write(data)
        else: #we get unexpected sequence number, send previous ack
            ack_packet = str(expected_seqnum -1) + 'acknowledgement'
            sent = sock.sendto(ack_packet, address)
            print "gg"
        
    except KeyboardInterrupt:
        raise
    except:
        print "exception"
        
        continue

file.close()
sock.close()
