import socket
import sys
import ast
 ###### ###### ###### ###### ######  helper functions START ###### ###### ###### ###### ###### ###### ###### 

def calculate_checksum(message):
    s = 0
    for i in range(0, len(message), 2):
        w = ord(message[i]) + (ord(message[i+1]) << 8) 
        s = (s + w & 0xffff) + (s + w >> 16)
    return ~s & 0xffff

# Extracts sequence number, ack data and checksum from a non-empty packet
def extract_packet(packet):
    seq_num = ast.literal_eval(packet[0])  #convert to int
    checksum = ast.literal_eval(packet[513:]) #convert to int
    return seq_num, packet[1:513], checksum 

 ###### ###### ###### ###### ######  helper functions END ###### ###### ###### ###### ###### ###### ###### 

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = ('localhost', 10000)
sock.bind(server_address)
corrupt = 0 ##if corrupt -> corrupt = 1
             ## corrupt also indicates whether we have correct seq_num or not
expected_seqnum = 0

while True:
    try:
        #get packet
        packet, address = sock.recvfrom(1000)
        if not packet:
            continue

        #extrack packet
        seq_num, data, checksum = extract_packet(packet)
        print seq_num

        print checksum
        #Check the data (sequence number, checksum)
        if seq_num != expected_seqnum or checksum != calculate_checksum(data):
            continue
        
        #make ack_packet and send back to client
        ack_packet = str(seq_num) + "acknowledgement"
        expected_seqnum += 1
        print "x"
        sent = sock.sendto(ack_packet, address)
        print data
        if expected_seqnum == 10:
            expected_seqnum = 0
    except:
        print "x"
        continue