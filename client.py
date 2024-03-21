from socket import *;

class Client:
    serverName = '127.0.0.1'
    serverPort = 5000

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    
    # assign a temporary port and save thec client data
    # in a table 
    sentence = input('Input lowercase sentence:')
    clientSocket.send(sentence.encode())
    modifiedSentence = clientSocket.recv(1024)

    print ('From Server:', modifiedSentence.decode())


    clientSocket.close()