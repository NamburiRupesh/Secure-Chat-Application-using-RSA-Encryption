import socket
import threading

def receive_messages(client_socket):
    """Receive messages from the server"""
    while True:
        try:
            message = client_socket.recv(1024).decode()  # Receiving data from server
            print(message)  # Print received messages to the user
        except:
            print("Disconnected from server.")  # If something goes wrong (like server disconnect)
            client_socket.close()  # Close socket connection
            break

def send_message(client_socket):
    """Send a message to the server"""
    while True:
        message = input("Enter message: ")  # Allow the user to type a message
        if message:
            client_socket.send(message.encode())  # Send the message to the server

def connect_to_server():
    """Connect to the server and handle login or registration"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 24345))  # Connect to the server at localhost on port 14345

    # Start threads for receiving and sending messages
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
    threading.Thread(target=send_message, args=(client_socket,), daemon=True).start()

    while True:
        # Receive the command and check which action to take
        message = input("Enter command (register, login, send_msg, create_group, join_group, expire_message, private_msg): ")
        
        if message.startswith('register'):
            client_socket.send(message.encode())  # Send registration request
        elif message.startswith('login'):
            client_socket.send(message.encode())  # Send login request
        elif message.startswith('send_msg'):
            client_socket.send(message.encode())  # Send regular message
        elif message.startswith('create_group'):
            client_socket.send(message.encode())  # Create a new group
        elif message.startswith('join_group'):
            client_socket.send(message.encode())  # Join an existing group
        elif message.startswith('expire_message'):
            client_socket.send(message.encode())  # Set expiration time for messages
        elif message.startswith('private_msg'):
            client_socket.send(message.encode())  # Send private message
        else:
            print("Invalid command! Please try again.")

if __name__ == "__main__":
    connect_to_server()  # Start the client connection process
