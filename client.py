import threading
from socket import *

class Client:
    def __init__(self, clientId, serverPort):
        self.serverName = '127.0.0.1'
        self.serverPort = serverPort
        self.clientId = clientId

        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.serverName, self.serverPort))

        self.clientSocket.send(str(self.clientId).encode())
        self.connectionAcknowledgement = self.clientSocket.recv(1024).decode()

    def send_message(self, recipientClientId):
        if self.connectionAcknowledgement == "Connected":
            print("In Client: ", self.clientId)
            inputMessage = input('Message?')
            message = f"{self.clientId}:{recipientClientId}:{inputMessage}"
            self.clientSocket.send(message.encode())
        else:
            print('Server Connection failed with Client: ', self.clientId)

    def receive_message(self):
        while True:
            try:
                messageReceived = self.clientSocket.recv(1024)
                if not messageReceived:
                    break
                print('From Server:', messageReceived.decode(), ' in client:', self.clientId)
            except Exception as e:
                print("Error occurred:", e)
                break

    def start_chat(self, recipientClientId):
        send_thread = threading.Thread(target=self.send_message, args=(recipientClientId,))
        receive_thread = threading.Thread(target=self.receive_message)

        send_thread.start()
        receive_thread.start()

        send_thread.join()
        receive_thread.join()

    def close_connection(self):
        self.clientSocket.close()
        print('Connection Closed')
