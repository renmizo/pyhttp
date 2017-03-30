#!/usr/bin/python3
import socket, threading
import time
import signal
import sys

class Threads(threading.Thread):

  #constructor for thread..
  def __init__(self,cliAddr,cliPort,cliConn):
    threading.Thread.__init__(self)
    self.cliAddr = cliAddr
    self.cliPort = cliPort
    self.cliConn = cliConn

  #main thread
  def run(self):
    print ("*************************************")
    print ("New thread started...\n")

    #socket information is extracted and displayed
    socketinfo  = str(socket.getaddrinfo(self.cliAddr,int(self.cliPort)))
    print ('Socket Info: \n' + socketinfo + '\n')

    #request is decoded and split to determine method
    reqRaw = self.cliConn.recv(1024)
    reqData = reqRaw.decode()
    reqMethod = reqData.split(' ')[0]
    datestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())

    #if get method supplied then run this
    if (reqMethod == 'GET'):

        #parse filename from data
        reqFile = reqData.split(' ')[1]

        #display connection info and file requested        
        print("Client IP: ", self.cliAddr)
        print("Client Port: ", self.cliPort)
        print("File Requested: ", reqFile)

        #format filename to work with script
        if(reqFile == '/'):
          reqFile = '/index.html'
        reqFile = '/www' + reqFile

        #open file for reading in binary mode
        try:
          with open(reqFile, 'rb') as myfile:
            data = myfile.read()
          
          #with no more data to read, close file
          myfile.close()

          print('Requested file found.  Code: 200\n')

          #build headers for a code rsponse of 200
          headers = ('HTTP/1.1 200 OK\n')
          headers += ('Date: ' + datestamp + '\n')
          headers += ('Server: My HTTP Server\n')
          headers += ('Connection: close\n\n')
          code = 200

        # if get method was supplied, but file not found
        except Exception as e:
          print('Requested file not found.  Code: 404\n', e)

          #build headers for a code of response of 404
          headers = ('HTTP/1.1 404 Not Found\n')
          headers += ('Date: ' + datestamp + '\n')
          headers += ('Server: My HTTP Server\n')
          headers += ('Connection: close\n\n')
          code = 404

    else:
        print('Bad request received.  Code: 400\n')

        #build headers for a code response of 400
        headers = ('HTTP/1.1 400 Bad Request\n')
        headers += ('Date: ' + datestamp + '\n')
        headers += ('Server: My HTTP Server\n')
        headers += ('Connection: close\n\n')
        code = 400

    #send headers before sending contents of file
    print('Sending headers with return code: ', code)
    self.cliConn.send(headers.encode())

    #test if code 200, then send contents of file
    if(code == 200):
      print('Sending data, contents of ', reqFile)
      self.cliConn.send(data)
    print ("*************************************")
    
    #display right before socket gets closed
    print ("Client at " + self.cliAddr + ":" + str(self.cliPort) + " disconnected...")

    #close down socket
    self.cliConn.close()

def Main():
  #host is hard coded, but port number is provided via command line argument
  host = '127.0.0.1'
  port = int(sys.argv[1])

  #socket is created using host and port args
  mySock = socket.socket()
  mySock.bind((host,port))

  print ("Listening on port " + str(port) + "...")

  #socket listens for incoming connections and creates threads
  while True:
    mySock.listen(1)
    cliConn, (cliAddr, cliPort) = mySock.accept()
    myThread = Threads(cliAddr,cliPort,cliConn)
    myThread.start()

if __name__ == '__main__':
  Main()
