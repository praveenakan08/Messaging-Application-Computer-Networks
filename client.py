from socket import *;

class Client:
    serverName = '127.0.0.1'
    serverPort = 5000

    # Whenever a client is created and its connected to the server
    def _init__(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.serverName, self.serverPort))
    
    #Function to send a message to client and recieve back the message from server
    def send_message(self, message):
        self.clientSocket.send(message.encode())
        modifiedSentence = self.clientSocket.recv(1024)
        print('From Server:', modifiedSentence.decode())
    
    def close_connection(self):
        self.clientSocket.close()