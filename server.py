import socket
import threading
import queue

class Server:
    def __init__(self, serverHost, serverserverPort):
        self.serverHost = serverHost
        self.serverPort = serverserverPort
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSockets = []
        self.globalBuffer = queue.Queue()  # Global frame buffer to store messages
        self.lock = threading.Lock()

    def handle_client(self, clientSocket):
        try:
            while True:
                data = clientSocket.recv(1024)
                if not data:
                    break
                message = data.decode()
                print(f"Received message from client: {message}")  #printing the message that Server recieves from the client   
                if message.strip().lower() == "exit":  #when client types exit it disconnects from server
                    print("Client requested disconnection.")
                    self.clientSockets.remove(clientSocket)
                    clientSocket.close()
                    break
                with self.lock:
                    self.globalBuffer.put((clientSocket, message))  # Putting the message into the queue along with client socket
        except Exception as e:
            print(f"Error handling client: {e}")
            clientSocket.close()
            self.clientSockets.remove(clientSocket)

    #Utlizing global buffer and sending messages to the clients
    def broadcast_messages(self):
        while True:
            try:
                clientSocket, message = self.globalBuffer.get(timeout=1)  #get messages from buffer
                print(f"Broadcasting message: {message}")
                with self.lock:
                    for sock in self.clientSockets:
                        if sock != clientSocket:  #Dont send the message to the sender client
                            try:
                                sock.sendall(message.encode())  #send message to other connected clients
                            except Exception as e:
                                print(f"Error broadcasting message to client: {e}")
                                sock.close()
                                self.clientSockets.remove(sock)
                                break
            except queue.Empty:
                continue

    #Method to accept connections from clients
    def accept_connections(self):
        try:
            self.serverSocket.bind((self.serverHost, self.serverPort))
            self.serverSocket.listen(5)
            print(f"Server listening on {self.serverHost}:{self.serverPort}")
            self.start_broadcasting()  # Start broadcasting messages

            while True:
                clientSocket, client_address = self.serverSocket.accept()
                print(f"Accepted connection from client: {client_address}")
                self.clientSockets.append(clientSocket)
                client_thread = threading.Thread(target=self.handle_client, args=(clientSocket,))
                client_thread.start()
        except Exception as e:
            print(f"Error accepting connection: {e}")

    def start_broadcasting(self):
        broadcast_thread = threading.Thread(target=self.broadcast_messages)
        broadcast_thread.daemon = True
        broadcast_thread.start()

    #When all the clients are disconnected server shutdowns
    def serverShutdown(self):
        try:
            self.serverSocket.close()
            for clientSocket in self.clientSockets:
                clientSocket.close()
            print("Server shutdown.")
        except Exception as e:
            print(f"Error shutting down server: {e}")
