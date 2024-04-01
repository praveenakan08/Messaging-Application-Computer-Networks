import sys
import threading
from server import Server
from client import Client

def client_task(client):
    client.connect_to_server()
    receive_msg_thread = threading.Thread(target=client.receive_messages)
    receive_msg_thread.start()

    while True:
        message = input(f"Client {client.clientId}: Enter your message or type 'exit' to disconnect from server\n")
        client.send_message(message)
        if message.lower() == "exit":
            client.disconnect_from_server()
            break

    receive_msg_thread.join()

def main():
    serverHost = 'localhost'#'127.0.0.1'
    serverPort = 5000

    #Start server and its worker threads to accept the connections
    server = Server(serverHost, serverPort)
    server_thread = threading.Thread(target=server.accept_connections)
    server_thread.start()

    #Take user input on how many clients to instantiate
    num_clients = int(input("Enter the number of clients to start: "))
    clients = []
    client_threads = []

    #For each client following tasks execute:
    #1.connect to the server
    #2.start sending messages to server
    #3.start recieving messages from peer clients
    
    for i in range(num_clients):
        clientId = i + 1
        client = Client(serverHost, serverPort, clientId)
        client_thread = threading.Thread(target=client_task, args=(client,))
        clients.append(client)
        client_threads.append(client_thread)
        client_thread.start()

    for thread in client_threads:
        thread.join()

    #Upon all the clients disconnection server shutsdown
    server.serverShutdown()

if __name__ == "__main__":
    main()
