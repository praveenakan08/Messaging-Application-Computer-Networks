from socket import *
import threading

class Client:
    def __init__(self, serverHost, serverPort, clientId):
        self.serverHost = serverHost
        self.serverPort = serverPort
        self.clientId = clientId
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.connected = False #Flag to check if its connected to server

    #Recieve messages from server
    def receive_messages(self):
        try:
            while True:
                data = self.clientSocket.recv(1024)
                if not data:
                    break
                message = data.decode()
                # Print received message form server
                print(f"Received message from server to Client {self.clientId}: {message}")
        except Exception as e:
            print(f"Error receiving message from server: {e}")

    #Send message to server
    def send_message(self, message):
        try:
            self.clientSocket.sendall(message.encode())
        except Exception as e:
            print(f"Error sending message to server: {e}")

    
    #Allowing clients to connecting to server
    def connect_to_server(self):
        try:
            self.clientSocket.connect((self.serverHost, self.serverPort))
            print(f"Client {self.clientId} connected to server")
            self.connected = True
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.start()  # Start receiving messages thread
        except Exception as e:
            print(f"Error connecting to server: {e}")


    #Allowing clients to disconnecting from server
    def disconnect_from_server(self):
        try:
            if self.receive_thread.is_alive():  # Check if the receive thread is alive before joining
                self.receive_thread.join()  # Wait for receive thread to finish
            self.clientSocket.close()
            print(f"Disconnected from server as Client {self.clientId}.")
        except Exception as e:
            print(f"Error disconnecting from server: {e}")
