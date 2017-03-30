#!/usr/bin/python3
import socket
import random
import sys
import time

def Main():
  #host, port, and filename vars are provided as args
  host = str(sys.argv[1])
  port = int(sys.argv[2])
  filename = str(sys.argv[3])

  print ("*************************************")
  print('Requesting ' + str(filename) + ' from ' + str(host) + ' on port ' + str(port))

  #socket is created using provided args
  mySock = socket.socket()
  mySock.connect((host,port))

  #socket information is extracted and displayed
  socketinfo = str(socket.getaddrinfo(host,int(port)))
  print ('\nSocket Info: \n' + socketinfo + '\n')

  #initial get header is constructed
  myMsg  = ('GET /' + filename + ' HTTP/1.1\n')
  myMsg += ('User-Agent: Python Client\n')

  #stamp time right before sending request
  xstart = time.time()

  #send request and headers to socket
  mySock.send(myMsg.encode())

  alldata = ''
  i = 0

  #loop to listen for all data returned, in 1024-byte chunks
  while True:
      chunk = mySock.recv(1024)

      #very first chunk received is used to calculate rtt
      if(i == 0):
          rtt = time.time()-xstart

      #for each iteration, chunk data is tacked onto end of alldata
      alldata += chunk.decode()
      i += 1

      #once data is no longer received, timestamp xfer end and exit
      if len(chunk) == 0:
        xend = time.time()
        break

  #calculate total file transfer time
  xtime = round(xend - xstart, 4)*1000

  #close out socket
  mySock.close()

  #parse header, grab code, and assign to code var
  code = int(alldata.split(' ')[1])

  #depending on code value 404,400,or 200, an if statement is chosen
  if(code == 404):
      print("File was not found on server.  Code 404\n")

  if(code == 400):
      print("Server responded with bad request.  Code 400\n")

  if(code == 200):
      print("File returned from server.  Code 200\n")
 
      #The raw data received is output to screen.
      print("Raw Output:\n")
      print(alldata)
      print ("\n*************************************")

      #Here the RTT is rounded and converted to milliseconds
      print('Rount Trip Time(RTT): ' + str(round(rtt,4)*1000) + ' ms')

      #Here the final calculations are shown
      print('Bytes received: ' + str(len(alldata)) + ' bytes')
      print('Transfer start: ' + str(xstart))
      print('Transfer end: ' + str(xend))
      print('Transfer length: ' + str(xtime) + ' ms')
      
  print ("*************************************\n\n")

if __name__ == '__main__':
  Main()

