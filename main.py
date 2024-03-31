from client import Client
import threading

# Create multiple clients with different ports
client1 = Client(1, 5000)
client2 = Client(2, 5000)

print("Client 1 ", client1.connectionAcknowledgement)
print("Client 2 ", client2.connectionAcknowledgement)

def start_chat(client, recipientClientId):
    client.start_chat(recipientClientId)

# Start the chat between client 1 and client 2
chat_thread1 = threading.Thread(target=start_chat, args=(client1, client2.clientId))
chat_thread2 = threading.Thread(target=start_chat, args=(client2, client1.clientId))

chat_thread1.start()
chat_thread2.start()

chat_thread1.join()
chat_thread2.join()

client1.close_connection()
client2.close_connection()
