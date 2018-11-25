import socket
import sys
from thread import *

# empty because it means we can listen any interface we choose
host = ""
port = 12344
#creating socket, second parameter means we will use TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")

try:
    #it is a data structure we're passing in that is
    #why there is a extra parantehses
    s.bind((host, port))
except:
    print("binding failed")
    #it is faied, quit from program
    sys.exit()
print("Socket has been bounded")

#  !!Now we can listen the client!!

#10 is random number, it means up to 10 client queued,
#11th connection is gonna rejected
s.listen(10)
print("socket is ready, (I am opening a socket for you bambo <3)")

def clientthread(conn):
    welcomeMessage = "Welcome to server, type something broo"
    conn.send(welcomeMessage)
    #while loop to get continuous stream of bytes
    while True:
        #we get 1024 byte data from connection
        data = conn.recv(1024)
        reply = "OK." + data.decode() #decode data to string
        if not data:
            break
        #reply and send data all of the connected client
        conn.sendall(data)
        print(reply) #print reply in the server
    #close socket connection
    conn.close()

#we will use connection variable that we're making here
# as well as address variable which stores the IP and port of
#the client that is trying to connect
conn, addr = s.accept()
while 1:
    #we will use connection variable that we're making here
    # as well as address variable which stores the IP and port of
    #the client that is trying to connect
    conn, addr = s.accept()
    #addr[0] -> IP of client
    #addr[1] -> port number
    print("Connected with " + addr[0] + ":" + str(addr[1]))
    start_new_thread(clientthread, (conn,))



  

#close socket it self
s.close()



