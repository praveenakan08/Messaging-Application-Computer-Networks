from socket import *;
import threading
import queue

class Server:
    def __init__(self):
        self.port = 5000 
        self.clients = {} # Dictionary to store connected clients and their ports
        self.frameBuffer = queue.Queue() # Queue for storing messages

    def start(self):
        # Create a socket for the server
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind(('localhost', self.port))
        self.serverSocket.listen(5)
        print("Server started on port", self.port)
        
        # connect to client requests
        while True:
            clientSocket, addr = self.serverSocket.accept()
            if not True:
                break  # Exit loop if server is stopped
            client_thread = threading.Thread(target=self.handle_client, args=(clientSocket,))
            client_thread.start()

    def handle_client(self, clientSocket):
        # Receive client id from client
        client_id = int(clientSocket.recv(1024).decode())
        
        # Store client's ID in the dictionary
        self.clients[client_id] = clientSocket
        
        # Receive and forward messages from the client
        while True:
            try:
                message = clientSocket.recv(1024).decode()
                if not message:
                    break
                self.frameBuffer.put((client_id, message))
                print("Client {} sent message: {}".format(client_id, message))
            except Exception as e:
                print("Error:", e)
                break
        
        # Remove client from dictionary when disconnected
        del self.clients[client_id]
        clientSocket.close()

    def stop(self):
        self.serverSocket.close()
