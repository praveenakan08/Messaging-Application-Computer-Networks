from socket import *;

class Client:
    def __init__(self, client_id):
        self.client_id = client_id
        self.serverPort = 5000  # Server port

    def start(self):
        # Connect to server
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect(('localhost', self.serverPort))
        
        # Send client ID to server
        self.clientSocket.send(str(self.client_id).encode())
        
        # Send messages to server
        while True:
            message = input("Enter message to send to server: ")
            if message == "exit":
                break
            self.clientSocket.send(message.encode())
        self.clientSocket.close()

    def exit(self):
        # Close the connection
        self.clientSocket.close()
