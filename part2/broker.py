from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM, timeout
from datetime import datetime
import sys
import time

##################        TIMER CLASS        ##################

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
    
    def set_timeout(self, duration):
        self._duration = duration

##################        TIMER CLASS        ##################

if len(sys.argv) < 2:
    sys.stderr.write(sys.argv[0] + " <file-to-be-written-in>\n")

SOCKET_SIZE = 1024
MAX_HEADER_SIZE = len("5000||65535")
WINDOW_SIZE = 10

estimated_rtt = 100.0
dev_rtt = 0.0
base = 0

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

#set window size
def set_window_size(num_packets):
    global base
    return min(WINDOW_SIZE, num_packets - base)

# Reliable Data Send over UDP connection
def rdt_send(seq, content, DEST):
    msg = str(seq) + "|" + content + "|"
    msg_send = msg + str(calculate_checksum(msg))

    #print seq, calculate_checksum(msg), len(remainder)

    tstart = datetime.now()
    send_sock.sendto(msg_send, DEST)

    # TODO: implement Go-Back-N method
    ack_received = False
    while not ack_received:
        try:
            message, address = recv_sock.recvfrom(SOCKET_SIZE)
            tend = datetime.now()
        except timeout: # In case of timeout, send the message again
            #print "Timeout"
            tstart = datetime.now()
            send_sock.sendto(msg_send, DEST)
        except KeyboardInterrupt:
            raise
        else:
            delta = tend - tstart
            rtt = float(float(delta.microseconds)/1000)
            #print "ACK message:", message, "(%f ms)" % rtt

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
    timer = Timer((estimated_rtt+4*dev_rtt)/1000.0) #recv_sock.settimeout((estimated_rtt+4*dev_rtt)/1000.0)

    tcp_sock.bind(SOURCE)
    tcp_sock.listen(1)

    connection, address = tcp_sock.accept()

    f = open(sys.argv[1], "w+")

    seq = 0
    remainder = ""
    base = 0
    next_to_send = 0
    window_size = 10
    done = 0 #If it becomes 1, bye byeee
    while True: # TODO: Implement for corrupt data
        
        while next_to_send < base + window_size:
            header_size = len(str(next_to_send) + "||" + str(2**16 - 1))
            print "aa"
            data = connection.recv(SOCKET_SIZE - MAX_HEADER_SIZE)
            msg = str(next_to_send) + "|" + data + "|"
            print "bb"
            msg_send = msg + str(calculate_checksum(msg))
            send_sock.sendto(msg_send, DEST)
            print "nextosend :  " +str(next_to_send)
            print "base :  " +str(base)
            print "window_size :  " +str(window_size)
            if not data:
                done = 1
                print "DONE"
                break
        
            if base == next_to_send:
                timer.start()
            next_to_send += 1
        print "GG"
        
        if done:
            break ## TODO SEND NULL MESSAGE to close file in destination
        
        if not timer.running():
            timer.start()
        
        while timer.running() and not timer.timeout():
            i = 0
            while i < window_size:
                ack_data, address = recv_sock.recvfrom(SOCKET_SIZE)
                try:
                    checksum = ack_data.split('|')[-1]
                    ack_seq = ack_data.split('|')[0]
                except:
                    break

                if ack_seq >= base:
                    base = ack_seq + 1

                    RTT = timer.get_rtt()
                    calculate_timeout(RTT)
                    timer.set_timeout((estimated_rtt+4*dev_rtt)/1000.0)
                    timer.stop()
                i+=1
        
        if timer.timeout():
            timer.stop()
            next_to_send = base

        ##TODO recv ack messages one time
        

    #       header_size = len(str(seq) + "||" + str(2**16-1))
    #       data = connection.recv(SOCKET_SIZE-MAX_HEADER_SIZE)
    #      
    #     if data:
    #        f.write(data)
        #     
        #      rdt_send(seq, data, DEST)
        #     seq += 1
        #else:
        #    break

        connection.sendall(data)

except:
    sys.stderr.write("Connection error\n")
finally:
    f.close()
    connection.close()

