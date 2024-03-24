from socket import *
import threading
import queue

class Server:
    serverPort = 5000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    print ('The server is ready to receive')

    # Global frame buffer(queue) for storing packets
    frame_buffer = queue.Queue()

    # Creating a map to keep track of connected clients
    clients_table = {}

    def create_thread(self):
        while true:
            connectionSocket, addr = serverSocket.accept()
            client=threading.Thread(target=handle_client,args=(connectionSocket, addr))
            client.start()

    def handle_client(self,connectionSocket,addr):
        client_port=addr[1]
        print('Client',addr,'connected')
        # Keep track of the client ports which are connected 
        # to the server in a table
        self.clients_table[client_port] = connectionSocket
        while True:
            sentence = connectionSocket.recv(1024).decode()
            # Store the data into buffer and forward packets
            # as they are received
            self.frame_buffer.put((client_port,sentence))

            #iterating over the buffer and checking for the given client if we have data to send and sending the data to server
            while not self.frame_buffer.empty():
                port, sentence = self.frame_buffer.get()
                for client_port, client_socket in self.clients_table.items():
                    if client_port != port:
                        capitalizedSentence = sentence.upper()
                        client_socket.send(capitalizedSentence.encode())

        del self.clients_table[client_port]
        print('Client', addr, 'disconnected')
        connectionSocket.close()
