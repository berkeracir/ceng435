import socket
import sys
import time
import thread

PACKET_SIZE = 512
ACK_PACKET_SIZE = 100
WINDOW_SIZE = 7
base = 0

#Timer class
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
#set window size, we need this because when we come to last packets,
# we need to make window size smaller
def set_window_size(num_packets):
    global base
    return min(WINDOW_SIZE, num_packets - base - 1)

#Calculates checksum
def calculate_checksum(message):
    s = 0
    for i in range(0, len(message), 2):
        w = ord(message[i]) + (ord(message[i+1]) << 8) 
        s = (s + w & 0xffff) + (s + w >> 16)
    return ~s & 0xffff

#Prepare packet which is -> sequence number|||data | checksum
def make_packet(seq_num, data, checksum):
    seq_bytes = str(seq_num)
    checksum_bytes = str(checksum)
    return seq_bytes + '|||' + data + ' | ' + checksum_bytes

#receive ack packets and update base according to that
def receive(sock):
    global mutex
    global base
    global timer

    while True:
        ack_data, server = sock.recvfrom(ACK_PACKET_SIZE)
        split = ack_data.find('|')
        seq_num = int(ack_data[:split])
        # If we get an ACK for the first in-flight packet
        print "seq ack  " + str(seq_num)
        print "base  " + str(base)
        if (seq_num >= base):
            mutex.acquire()
            base = seq_num + 1
            print('Base updated', base)
            timer.stop()
            mutex.release()

 ###### ###### ###### ###### ###### ###### helper functions END ###### ###### ###### ###### ###### ###### 

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 10000) ##localhost, portnumber

timer = Timer(1) #implies that timeout is 1 sec


#first thing that we are going to do is packetizing
mutex = thread.allocate_lock()
a = open("3.txt", "w+")
try:
    # Open file
    with open(sys.argv[1]) as f: 
        #packetize the data till to the end
        i=0
        global mutex
        global base
        global send_timer
        seq_num = 0 # sequence number 0 to 9
        packets = [] #list of all packets, because before sending any data,

        while True:
            #read PACKET_SIZE byte data from file
            message = f.read(PACKET_SIZE) 
            if not message:
                break
            #add to packets list with sequence number and checksum
            packets.append(make_packet(seq_num, message, calculate_checksum(message)))
            seq_num += 1

        next_to_send = 0 #next packet's sequence number that we are going to send
        num_packets = len(packets)   
        window_size = set_window_size(num_packets) #set window size
        thread.start_new_thread(receive, (sock, ))   #start receiver function, we use it to get ack messages
        base = 0
        while base < num_packets:
            mutex.acquire()#lock
            print "lock for get data"
            #there are packet that we can send, send till end of window
            if next_to_send == num_packets:
                break
            
            while next_to_send < base + window_size:
                if next_to_send == num_packets:
                    break 
                sent = sock.sendto(packets[next_to_send], server_address)
                if base == next_to_send:
                    timer.start()
                print next_to_send    
                next_to_send += 1
            #start timer if is not running
            if not timer.running():
                print 'start timer'#for debug 
                timer.start()
           
           #if timer is running and not timeout, stop this loop for 0.05 sec, let receive function run.
           #Get ack messages from there
            while timer.running() and not timer.timeout():
                mutex.release()
                time.sleep(0.05) #let receive function run for this 0.05 sec
                mutex.acquire()
            
            #we fucked up, send all message again
            if timer.timeout():
                print 'stop timer and set base to beginning'#for debug 
                timer.stop()
                next_to_send = base           
            else:
                window_size = set_window_size(num_packets) # set new window size.NOTE It does not change until last packets
            
            mutex.release() #release

        # send null message to close server, with that null message we indicate that we send all packets
     
finally:
    print >>sys.stderr, 'closing socket'
    sock.close()

