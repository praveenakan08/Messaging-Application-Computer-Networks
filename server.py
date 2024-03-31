from socket import *

class Server:
    def __init__(self):
        self.serverPort = 5000
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind(('', self.serverPort))
        self.serverSocket.listen(1)
        print('The server is ready to receive')

        self.clients = {}

    def accept_connections(self):
        while True:
            clientSocket, addr = self.serverSocket.accept()
            print("Connected from: ", addr)

            clientId = clientSocket.recv(1024).decode()
            self.clients[clientId] = clientSocket
            clientSocket.send(str("Connected").encode())
            print(self.clients.keys)
            if len(self.clients) == 2: 
                break

    def handle_messages(self):
        while True:
            clients_copy = dict(self.clients)
            for clientId, clientSocket in clients_copy.items():
                try:
                    data = clientSocket.recv(1024).decode()
                    if not data:
                        continue
                    
                    senderId, recipientId, message = data.split(":") 
                    if senderId in clients_copy:
                        recipientSocket = clients_copy.get(recipientId)

                        if recipientSocket:
                            recipientSocket.sendall(message.upper().encode())
                            print("Forwarded message to Client with ClientId: ", recipientId)
                        else:
                            print("Recipient with ID", recipientId, " not found")
                            break
                except Exception as e:
                    print("Error occurred:", e)


# Start the server
server = Server()

server.accept_connections()
# Handle messages in the main thread
server.handle_messages()
