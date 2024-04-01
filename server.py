import socket
import threading
import queue

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sockets = []
        self.frame_buffer = queue.Queue()  # Global frame buffer to store messages
        self.lock = threading.Lock()  # Lock to ensure thread-safe access to the frame buffer

    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print(f"Received message from client: {message}")  # Print received message
                if message.strip().lower() == "exit":  # Special message to disconnect
                    print("Client requested disconnection.")
                    self.client_sockets.remove(client_socket)
                    client_socket.close()
                    break
                with self.lock:
                    for client in self.client_sockets:
                        if client != client_socket:  # Exclude the sender
                            try:
                                client.sendall(data)  # Broadcast message to other clients
                            except Exception as e:
                                print(f"Error broadcasting message to client: {e}")
                                client.close()
                                self.client_sockets.remove(client)
                                break
        except Exception as e:
            print(f"Error handling client: {e}")
            client_socket.close()
            self.client_sockets.remove(client_socket)

    def accept_connections(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"Server listening on {self.host}:{self.port}")

            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Accepted connection from client: {client_address}")
                self.client_sockets.append(client_socket)
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
        except Exception as e:
            print(f"Error accepting connection: {e}")

    def shutdown(self):
        try:
            self.server_socket.close()
            for client_socket in self.client_sockets:
                client_socket.close()
            print("Server shutdown.")
        except Exception as e:
            print(f"Error shutting down server: {e}")
