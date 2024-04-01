import sys
import threading
from server import Server
from client import Client

# main.py

def client_task(client):
    client.connect()
    receive_thread = threading.Thread(target=client.receive_messages)
    receive_thread.start()

    while True:
        message = input(f"Client {client.client_id}: Enter your message (type 'exit' to quit): ")
        client.send_message(message)
        if message.lower() == "exit":
            client.disconnect()
            break

    receive_thread.join()  # Wait for the receive thread to finish


# main.py

def main():
    server_host = '127.0.0.1'
    server_port = 12345

    # Start the server
    server = Server(server_host, server_port)
    server_thread = threading.Thread(target=server.accept_connections)
    server_thread.start()

    # Start multiple clients
    num_clients = int(input("Enter the number of clients to start: "))
    clients = []
    client_threads = []

    for i in range(num_clients):
        client_id = i + 1
        client = Client(server_host, server_port, client_id)
        client_thread = threading.Thread(target=client_task, args=(client,))
        clients.append(client)
        client_threads.append(client_thread)
        client_thread.start()

    for thread in client_threads:
        thread.join()

    server.shutdown()  # Move server shutdown outside the loop

if __name__ == "__main__":
    main()
