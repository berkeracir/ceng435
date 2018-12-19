import socket
import sys
import thread
import datetime as dt
from time import sleep
import os
#Initialize the socket size
SOCKET_SIZE = 1024
#Check arguments. If we do not get enough argument, exit from script.
# We need to get destination1&desnation2 port number's and IP's and file to save data that we receive
# Note that we gave this arguments in our script which executes all nodes
if len(sys.argv) < 6:
    print "Expected Arguments:", sys.argv[0], "<DESTINATION1-IP>", "<DESTINATION1-PORT>", "<DESTINATION2-IP>", "<DESTINATION2-PORT>", "<SAVE-FILE-NAME>"
    sys.exit()

# Initialize addresses with given parameters
destination1_address = (sys.argv[1], int(sys.argv[2]))
destination2_address = (sys.argv[3], int(sys.argv[4]))
#initialize total delay and count which is total number of packets
total_delay = 0.0
count = 0

def clientThread(data, address, time):
    global total_delay
    global save_file
    #Get the current time with microseconds
    msg_time = dt.datetime.strptime(data.split('|')[1], "%Y/%m/%d %H:%M:%S.%f")
    #Calculate the delay
    time_diff = time - msg_time
    #Convert the delay to microseconds
    delay_in_ms = time_diff.days*24*60*60*1000 + time_diff.seconds*1000 + time_diff.microseconds/1000.0
    #Add packet delay to total delay
    total_delay += delay_in_ms
    print "Received Message:", data.split('|')[0], "at:", time.strftime("%Y/%m/%d %H:%M:%S.%f"), "\n\tfrom:", address, "\n\ttime diff:", delay_in_ms, "ms"
    #Save delay to file
    save_file.write(str(delay_in_ms) + "\r\n")

def serverThread(address):
    global count
    # Create socket with UDP connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to address router address
    # In case of fail, exit from script
    try:
        sock.bind(address)

        while True:
            #Receive data and address from connected socket
            data, address = sock.recvfrom(SOCKET_SIZE)
            time = dt.datetime.utcnow()
            #If there exist data, increase the packet number and open thread 
            #Send data, address and current time information to that thread function.
            if data:
                count += 1
                thread.start_new_thread(clientThread, (data, address, time, ))
    except:
        print "Socket Binding Exception:", address
        sys.exit()
    
try:
    #Open the file for writing with second parameter
    save_file = open(sys.argv[5], "w+")
    #Start 2 thread, first one gets data from router 1, second one gets data from router 2
    thread.start_new_thread(serverThread, (destination1_address, ))
    thread.start_new_thread(serverThread, (destination2_address, ))

    while True:
        #Calculate the average delay
        try:
            avg = total_delay/count
        except ZeroDivisionError:
            avg = 0
        
        print "Average Delay:", avg, "ms (" + str(total_delay) + " ms/" + str(count) + ")"
        #After receiving completed, wait for client threads to complete writing delay informations to file
        os.system("wc -l " + sys.argv[5])
        sleep(10)
#Close the file after all done
finally:
    save_file.close()

## Information about threads' purposes:
    ## We open 2 server thread for router 1 and router 2
    ## In server thread we get information from router seperately.
    ## Everytime we get data, we open client thread.
    ## Client thread calculates the total delay and writes to the file.