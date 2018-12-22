import socket
import sys
import time
import ast

PACKET_SIZE = 512
ACK_PACKET_SIZE = 100

class Timer(object):
    TIMER_STOP = -1
    
    def __init__(self, duration):
        self._start_time = self.TIMER_STOP
        self._duration = duration

    # Starts the timer
    def start(self):
        if self._start_time == self.TIMER_STOP:
            self._start_time = time.time()

    # Stops the timer
    def stop(self):
        if self._start_time != self.TIMER_STOP:
            self._start_time = self.TIMER_STOP

    # Determines whether the timer is runnning
    def running(self):
        return self._start_time != self.TIMER_STOP

    # Determines whether the timer timed out
    def timeout(self):
        if not self.running():
            return True
        else:
            return time.time() - self._start_time >= self._duration
    
    #return time difference if timer is running
    def get_rtt(self):
        if self.running():
            return time.time() - self._start_time
        else:
            return -1

 ###### ###### ###### ###### ######  helper functions START ###### ###### ###### ###### ###### ###### ###### 

def calculate_checksum(message):
    s = 0
    for i in range(0, len(message), 2):
        w = ord(message[i]) + (ord(message[i+1]) << 8) 
        s = (s + w & 0xffff) + (s + w >> 16)
    return ~s & 0xffff

def make_packet(seq_num, data, checksum):
    seq_bytes = str(seq_num)
    checksum_bytes = str(checksum)
    return seq_bytes + data + ' | ' + checksum_bytes

 ###### ###### ###### ###### ###### ###### helper functions END ###### ###### ###### ###### ###### ###### 

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 10000) ##localhost, portnumber
sock.settimeout(0.5)

timer = Timer(1) #implies that timeout is 0.5 sec
expected_seqnum = 0
seq_num = 0 # sequence number 0 to 9
packets = []

base = 0


a = open("sourcedata.txt", "w+")

try:
    # Open file
    with open(sys.argv[1]) as f: 
        #packetize the data till to the end
        i=0
        while True:
            message = f.read(PACKET_SIZE) 
            if not message:
                break
            packets.append(make_packet(seq_num, message, calculate_checksum(message)))
            seq_num += 1
            if seq_num == 10:
                seq_num = 0

            i+=1
            a.write(message)

        num_packet = len(packets)      
        i = 0   
        while i < num_packet:
            #send message and start timer
            sent = sock.sendto(packets[i], server_address)
            timer.stop()  #stop timer if it is running
            timer.start() #start timer for packet
            corrupt = 0
            print('packet number:'  +(packets[i][0]))
            #wait for response until timeout    
            while timer.timeout() != True:
                try:
                    ack_data, server = sock.recvfrom(ACK_PACKET_SIZE) #receive data
                    #extract ack packet, first char is sequence number, 1 to 4(3 char) is 'ACK', 4 to end is checksum
                    seq_num, ack_message = int(ack_data[0]), ack_data[1:16] #ast.literal_eval -> convert to int
                    #check sequence number and checksum and timeout value                   
                    if (seq_num != expected_seqnum):
                        corrupt = 1
                        break
                    
                    #get rtt and stop timer, we can send next packet
                    rtt = timer.get_rtt()
                    timer.stop()

                    expected_seqnum += 1
                    if expected_seqnum == 10:
                        expected_seqnum = 0
                except:
                    continue  

            #if there is a timeout or packet is corrupt, send packet again
            if timer.running() == False and corrupt == 0:
                i += 1   

        sent = sock.sendto('0' + 'NULLMESSAGE' + ' | ' + '0', server_address)      
finally:
    print >>sys.stderr, 'closing socket'
    sock.close()

