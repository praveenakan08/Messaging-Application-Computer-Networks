## Github Link
https://github.com/praveenakan08/Messaging-Application-Computer-Networks

## Clone this project by using:
git clone https://github.com/praveenakan08/Messaging-Application-Computer-Networks

## Run this project using the following command:
python main.py

## How it works
The server listens for incoming connections from nodes on a specified port.

Each node connects to the server.

Nodes can send messages through the server, which forwards them to all the other clients.

The server maintains a table to track connected nodes and their ports.

To handle concurrent communication between the nodes, server runs worker threads.

The server uses a global frame buffer (queue) to store messages for forwarding messages.

The code allows for flexible node instantiation between 2 and 255.
