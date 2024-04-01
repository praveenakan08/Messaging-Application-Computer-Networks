import socket
import threading

class Client:
    def __init__(self, host, port, client_id):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.connected = False

    def receive_messages(self):
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print(f"Received message from server: {message}")
        except Exception as e:
            print(f"Error receiving message from server: {e}")



    def send_message(self, message):
        try:
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message to server: {e}")

    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to server as Client {self.client_id}.")
            self.receive_thread.start()  # Start receiving messages thread
            self.connected = True
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def disconnect(self):
        try:
            if self.receive_thread.is_alive():  # Check if the receive thread is alive before joining
                self.receive_thread.join()  # Wait for receive thread to finish
            self.client_socket.close()
            print(f"Disconnected from server as Client {self.client_id}.")
        except Exception as e:
            print(f"Error disconnecting from server: {e}")



