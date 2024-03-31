from client import Client
import threading

# Create multiple clients with different ports
client2 = Client(2, 5000)

print("Client 2 ", client2.connectionAcknowledgement)

send_message_thread = threading.Thread(target=client2.send_message)
receive_message_thread = threading.Thread(target=client2.receive_message)

send_message_thread.start()
receive_message_thread.start()
