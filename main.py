import sys
import threading
from server import Server
from client import Client

def signal_clients_exit(clients):
    for client in clients:
        client.exit()  # Call the exit method in the client class to handle cleanup

#provide no. of clients to instantiate
if len(sys.argv) < 2:
    print("Provide atleast 2 clients for Messaging!")

#take user input
num_clients = int(sys.argv[1])
if num_clients < 2 or num_clients > 255:
    print("Number of clients must be between 2 and 255.")

# Start server
server = Server()
server_thread = threading.Thread(target=server.start)
server_thread.start()

# Start clients
clients = []
client_threads = []
for i in range(1, num_clients+1):
    client = Client(i)
    client_thread = threading.Thread(target=client.start)
    client_thread.start()
    clients.append(client)  # Store client objects
    client_threads.append(client_thread)  # Store Thread objects

# Wait for each of the clients to finish
for client_thread in client_threads:
    client_thread.join()

#exit client
signal_clients_exit(clients)

# Stop server
server.stop()
