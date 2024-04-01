import socket
import threading
import queue

class Server:
    def __init__(self, serverHost, serverserverPort):
        self.serverHost = serverHost
        self.serverPort = serverserverPort
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsTable = []
        self.globalBuffer = queue.Queue()  # Global frame buffer to store messages
        self.lock = threading.Lock()

    # Adding connected clients to clientsTable and storing the received messages from clients into the global buffer
    def handle_client(self, clientSocket):
        try:
            while True:
                data = clientSocket.recv(1024)
                if not data:
                    break
                message = data.decode()
                print(f"Received message from client: {message}")  # Printing message received from client  
                if message.strip().lower() == "exit":  # Removing client from clientsTable (as requested from client) 
                    print("Client requested disconnection.")
                    self.clientsTable.remove(clientSocket)
                    clientSocket.close()
                    break
                with self.lock:
                    self.globalBuffer.put((clientSocket, message))  # Appending the received message to the global buffer
        except Exception as e:
            print(f"Error handling client: {e}")
            clientSocket.close()
            self.clientsTable.remove(clientSocket)

    # Utlizing global buffer and sending messages to the clients
    def broadcast_messages(self):
        while True:
            try:
                senderClient, message = self.globalBuffer.get(timeout=1)  # Get messages from buffer
                print(f"Broadcasting message: {message}")
                with self.lock:
                    for connectedClient in self.clientsTable:
                        if connectedClient != senderClient:  # Making sure that the senderClient is not the receiving client
                            try:
                                connectedClient.sendall(message.encode())  # Send message to other connected clients
                            except Exception as e:
                                print(f"Error broadcasting message to client: {e}")
                                connectedClient.close()
                                self.clientsTable.remove(connectedClient)
                                break
            except queue.Empty:
                continue

    # Method to accept connections from clients
    def accept_connections(self):
        try:
            self.serverSocket.bind((self.serverHost, self.serverPort))
            self.serverSocket.listen(5)
            print(f"Server listening on {self.serverHost}:{self.serverPort}")
            self.start_broadcasting()  # Start broadcasting messages to all connected clients

            while True:
                clientSocket, client_address = self.serverSocket.accept()
                print(f"Accepted connection from client: {client_address}")
                self.clientsTable.append(clientSocket)
                client_thread = threading.Thread(target=self.handle_client, args=(clientSocket,))
                client_thread.start()
        except Exception as e:
            print(f"Error accepting connection: {e}")

    # Helper method to start broadcasting messages
    def start_broadcasting(self):
        broadcast_thread = threading.Thread(target=self.broadcast_messages)
        broadcast_thread.daemon = True
        broadcast_thread.start()

    # Shutting server down, when all clients are disconnected
    def serverShutdown(self):
        try:
            self.serverSocket.close()
            for clientSocket in self.clientsTable:
                clientSocket.close()
            print("Server shutdown.")
        except Exception as e:
            print(f"Error shutting down server: {e}")
