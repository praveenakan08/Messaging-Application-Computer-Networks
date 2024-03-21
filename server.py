from socket import *

class Server:
    serverPort = 5000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    print ('The server is ready to receive')

    while True:
        connectionSocket, addr = serverSocket.accept()
        sentence = connectionSocket.recv(1024).decode()
        # Add thread functionality to perform server task
        capitalizedSentence = sentence.upper()
        # Store the data into buffer and forward packets
        # as they are received
        
        # Keep track of the client ports which are connected 
        # to the server in a table
        connectionSocket.send(capitalizedSentence.encode())

    connectionSocket.close()
