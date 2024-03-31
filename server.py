from socket import *
import queue
import threading
import time

class Server:

    def __init__(self):
        self.serverPort = 5000
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind(('', self.serverPort))
        self.serverSocket.listen(5)
        print('The server is ready to receive')
        self.clients = {}
        self.frameBuffer = queue.Queue() 
        self.lock = threading.Lock()
    
    def accept_connections(self):
        while True:
            clientSocket, addr = self.serverSocket.accept()
            print("Connected from: ", addr)
            clientId = clientSocket.recv(1024).decode()
            self.clients[clientId] = clientSocket
            clientSocket.send(str("Connected").encode())
    
    def handle_messages(self):
        while True:
            clients_copy = dict(self.clients)
            print(clients_copy)
            for clientId, clientSocket in clients_copy.items():
                try:
                    data = clientSocket.recv(1024).decode()
                    if not data:
                        continue
                    
                    senderId, recipientId, message = data.split(":") 
                    if senderId in clients_copy:
                        recipientSocket = clients_copy.get(recipientId)
                        if recipientSocket:
                            self.frameBuffer.put((recipientSocket, message))
                        else:
                            print("Recipient with ID", recipientId, " not found")
                except Exception as e:
                    print("Error occurred:", e)
            time.sleep(1)

    def send_messages_from_buffer(self):
        while True:
            while not self.frameBuffer.empty():
                    message = self.frameBuffer.get()
                    message[0].sendall(message[1].encode())
                    print('Message sent to client', message[0])
server = Server()

connections_accept_thread = threading.Thread(target=server.accept_connections)
messages_handle_thread = threading.Thread(target=server.handle_messages)
send_messages_from_buffer_thread = threading.Thread(target=server.send_messages_from_buffer)

connections_accept_thread.start()
messages_handle_thread.start()
send_messages_from_buffer_thread.start()