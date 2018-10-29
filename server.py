import socket
import sys
from thread import *
import threading

HOST = ''
NAME = ''
PORT = int(sys.argv[1])
IPAddr1 = sys.argv[2]
MacAddr1 = sys.argv[3]
Priority = 32768
BridgeID = str(Priority) + MacAddr1
self = PORT - 7999
PORTSTATUS = []
rootBID = BridgeID
rootCost = 0

NODE = []
MAP = [[3, 4, 2], [4, 3, 1], [1, 2, 4], [2, 1, 3]]

IP = []
for x in range(0, 4):
    NODE.append(x+1)
    IP.append('10.0.0.' + str(x + 1))

myList = []
reply2 = []

BPDU = BridgeID + ' ' + str(rootCost) + ' ' + rootBridge + ' ' + self

MacAddr2 = []


for x in range(1, 4):
   MacAddr2.append('')
   PORTSTATUS.append(1)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'

try:
  s.bind((HOST, PORT))
except socket.error, msg:
   print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
   sys.exit()
print 'socket bind complete'

s.listen(10)
print 'Socket now listening'

def set_timer():
      threading.Timer(5.0, set_timer).start()
      if rootBID == BridgeID:
	   for x in range(0, 4):
     	       if x != self:
		    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		    serv.connect(('localhost', 8000 + x))
		    serv.send(BPDU)
		    serv.close()
      print 'MAC\t\t\tNODE\t\t\tSTATUS\n'
      for x in range (0, 3):
	print MacAddr2[x] + '\t\t\t' + NODE[x] + '\t\t\t' + PORTSTATUS[x]

def clientthread(conn):
#   conn.send('Welcome to the server. Type something and hit enter\n')
      while True:
		
	data = conn.recv(1024)
#	print data[0:18]
	send = False
	numPort = 0
	newID = data.split(' ')
	#check = true
	numPort = newID[3] - 1
	if MacAddr2[numPort] == '':
	   MacAddr2[numPort] = newID[0][5:]
	#for x in range(1, 4):
	 #   if str(newID[0][5:]) == MacAddr2[x]:
	#	numPort = x
	#	check = false
	#	break
	#if check:
	 #   for x in range(1, 4):
	  #  	if MacAddr2[x] == '':
	#	    MacAddr2[x] = str(newID[0][5:])
	#	    numPort = x
	#	    break
	if PORTSTATUS[newID[3]] < 0:
	   continue
	elif int(newID[2][0:9]) < int(BridgeID[0:9]):
	   rootBID = newID[2]
	   rootCost = int(newID[1] + 1)
	   PORTSTATUS[numPort] = 0
	   BPDU = BridgeID + ' ' + rootCost + ' ' + rootBID + ' ' + self
	   for y in range(1, 4):
		if x != y and PORTSTATUS[y] == 0:
		   PORTSTATUS[y] = 1
		   send = True
	elif int(newID[2][0:9]) == int(BridgeID[0:9]) and int(newID[1]) < rootCost:
	   rootBID = newID[2]
	   rootCost = int(newID[1]) + 1
	   PORTSTATUS[numPort] = -1
	   BPDU = BridgeID + ' ' + rootCost + ' ' + rootBID + ' ' + self
	   send = True
	elif int(newID[2][0:9]) == int(BridgeID[0:9]) and int(newID[1]) == rootCost and int(newID[0][0:9]) < int(BridgeID[0:9]):
	   rootBID = newID[2]
	   rootCost = int(newID[1]) + 1
	   PORTSTATUS[numPort] = -1
	   BPDU = BridgeID + ' ' + rootCost + ' ' + rootBID + ' ' + self
	   send = True
	if send == True:
	   for x in range(1, 4) and newID[3] != MAP[self - 1][x]:
		if PORTSTATUS[x] == 1:
		   serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		   serv.connect(('localhost', MAP[self - 1][x] + 7999))
		   serv.send(BPDU)
		   serv.close()
	if not data:
	   break

#	conn.sendall(reply)
        #print data
      conn.close()

while 1:
   conn, addr = s.accept()
   print 'Connected with ' + addr[0] + ':' + str(addr[1])
   set_timer()
   start_new_thread(clientthread ,(conn,))
   myList.append(conn)
s.close()
