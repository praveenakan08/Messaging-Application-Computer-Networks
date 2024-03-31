from socket import *;
import threading

class Client:
    def __init__(self, clientId, serverPort):
        self.serverName = '127.0.0.1'
        self.serverPort = serverPort
        self.clientId = clientId

        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.serverName, self.serverPort))

        self.clientSocket.send(str(self.clientId).encode())
        self.connectionAcknowledgement = self.clientSocket.recv(1024).decode()

    def send_message(self):
        if self.connectionAcknowledgement == "Connected":
            while True:
                print("In Client: ", self.clientId)
                choice = input("Want to send a message? (y/n)")

                if choice == 'y':
                    recipientClientId = int(input("Which client?"))
                    inputMessage = input('Message?')
                    message = f"{self.clientId}:{recipientClientId}:{inputMessage}"
                    self.clientSocket.send(message.encode())
                else:
                    print('Message session with client: ', self.clientId, ' has ended')
                    break
        else:
            print('Server Connection failed with Client: ', self.clientId)

    def receive_message(self):
        while True:
            try:
                messageReceived = self.clientSocket.recv(1024)
                print('From Server:', messageReceived.decode(), ' in client:', self.clientId)
            except Exception as e:
                print("Error occurred:", e)
                break