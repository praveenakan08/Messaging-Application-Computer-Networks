from client import Client
import threading

# Create multiple clients with different ports
client1 = Client(1, 5000)

print("Client 1 ", client1.connectionAcknowledgement)

send_message_thread = threading.Thread(target=client1.send_message)
receive_message_thread = threading.Thread(target=client1.receive_message)

send_message_thread.start()
receive_message_thread.start()
