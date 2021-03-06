import socket
import sys
import time
import math

class Queue:
  #Constructor creates a list
  def __init__(self):
      self.queue = list()

  #Adding elements to queue
  def enqueue(self,data):
      #Checking to avoid duplicate entry (not mandatory)
      if data not in self.queue:
          self.queue.insert(0,data)
          return True
      return False

  #Removing the last element from the queue
  def dequeue(self):
      if len(self.queue)>0:
          return self.queue.pop()
      return ("Queue Empty!")

  #Getting the size of the queue
  def size(self):
      return len(self.queue)

  #printing the elements of the queue
  def printQueue(self):
      return self.queue

class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

#Instanitate CPU values
politicaCPU = "RR" #Round Robin
politicaMEM = "MFU" #Most Frequently used
quantum = 1.0 #quantum size in seconds
realMem = 3 #real memory size in kilonytes, 1 => 1024
swapMem = 4 #swap memory size in kilobytes, 1 => 1024
pageSize = 1 #page size in kilobytes, 1 => 1024
timestamp = 0.0
delta = quantum

pageTable = ["L"] * (realMem/pageSize) #lista con paginas inicialmente libres
mfuPageTable = Stack()
swapTable = ["L"] * (swapMem/pageSize) #lista de swap inicialmente libre
mfuSwapTable = Stack()
pQueue = Queue() #cola de listos
CPU = "L"
processID = 1
processSize = ["L"]

def incrementTimestamp(time):
	global timestamp
	timestamp += time

def resetDelta():
	global delta
	delta = quantum

def decrementDelta():
	global delta
	delta -= quantum

def addPage(processID, pageID):
	global pageTable
	# processName = str(processID) + "."
	# processMatching = [s for s in pageTable if processName in s]
	tableEntry = str(processID) + "." + str(pageID)
	if tableEntry in pageTable:
		#nothing, page already loaded
		print("Page already in Real Memory")

	else:
		print("Page Fault in Real Memory")
		#memoria libre
		if "L" in pageTable:
			i = pageTable.index("L")
			pageTable[i] = tableEntry
		#memoria ocpada, necesidad de un swap
		else:
			print("Swap in page table, PENDING LOGIC")

	return tableEntry

def addQueueProcToCPU():
	topProcessID = pQueue.dequeue()
	CPU = (addPage(topProcessID, 0))

def create(size):
	global processID
	global CPU
	global processSize
	processSize.append(int(math.ceil(float(size))))
	pQueue.enqueue(processID)

	#if first process
	if CPU == "L":
		addQueueProcToCPU()

	print >>sys.stderr, 'sending answer back to the client'
	answer = "%.3f process %s created size %s pages" % (timestamp, processID, processSize[processID])
	connection.sendall(answer)
	processID += 1

def address(processID, virtualAddress):
	print(address)
	#process not in CPU
	#virtual address out of bounds

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Then bind() is used to associate the socket with the server address. In this case, the address is localhost, referring to the current server, and the port number is 10000.

# Bind the socket to the port
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)


#Calling listen() puts the socket into server mode, and accept() waits for an incoming connection.

# Listen for incoming connections
sock.listen(1)


# Wait for a connection
print >>sys.stderr, 'waiting for a connection'
connection, client_address = sock.accept()

#accept() returns an open connection between the server and client, along with the address of the client. The connection is actually a different socket on another port (assigned by the kernel). Data is read from the connection with recv() and transmitted with sendall().

try:
	print >>sys.stderr, 'connection from', client_address

    # Receive the data
	while True:
		data = connection.recv(256)
		if data == "":
			print >>sys.stderr, 'no data from', client_address
			connection.close()
			sys.exit()
		command = data
		comment = None
		parameters = []

		if "//" in command:
			commentSplit = data.split("//")
			command = commentSplit[0]
			comment = commentSplit[1]
		if " " in  command:
			parameters = commentSplit[0].split(" ")
			command = parameters[0]

		incrementTimestamp(0.001)
		#Create %s, size in pages
		if command == "Create":
			create(parameters[1])
		#Quantum
		if command == "Quantum":
			print("Quantum")
		#Address
		if command == "Address":
			address(command, parameters[1], parameters[2])
		#Fin
		#End


finally:
     # Clean up the connection
	print >>sys.stderr, 'se fue al finally'
	connection.close()

#When communication with a client is finished, the connection needs to be cleaned up using close(). This example uses a try:finally block to ensure that close() is always called, even in the event of an error.


def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
