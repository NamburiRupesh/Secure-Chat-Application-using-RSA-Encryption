import socket
import threading
import time
import datetime

clients = {}
groups = {}
message_expiry = {}

def broadcast(message, client_socket=None):
    """Send message to all clients except the sender"""
    for client, details in clients.items():
        if client != client_socket:
            try:
                client.send(message.encode())
            except:
                client.close()
                remove_client(client)

def remove_client(client_socket):
    """Remove client from the list when they disconnect"""
    if client_socket in clients:
        del clients[client_socket]

def handle_private_message(client_socket, recipient, message):
    """Send private message to a specific user"""
    found = False
    for client, details in clients.items():
        if details['username'] == recipient:
            try:
                client.send(f"Private message from {clients[client_socket]['username']}: {message}".encode())
                found = True
                break
            except:
                client.close()
                remove_client(client)
    if not found:
        client_socket.send(f"User {recipient} not found.".encode())

def create_group(client_socket, group_name):
    """Allow the client to create a group"""
    if group_name not in groups:
        groups[group_name] = [clients[client_socket]['username']]
        client_socket.send(f"Group '{group_name}' created.".encode())
    else:
        client_socket.send(f"Group '{group_name}' already exists.".encode())

def join_group(client_socket, group_name):
    """Allow the client to join an existing group"""
    if group_name in groups:
        if clients[client_socket]['username'] not in groups[group_name]:
            groups[group_name].append(clients[client_socket]['username'])
            client_socket.send(f"Joined group '{group_name}'.".encode())
        else:
            client_socket.send(f"You're already in the group '{group_name}'.".encode())
    else:
        client_socket.send(f"Group '{group_name}' does not exist.".encode())

def remove_expired_messages():
    """Remove expired messages from the message_expiry dictionary"""
    while True:
        current_time = datetime.datetime.now()
        to_remove = []
        for message_time, username in message_expiry.items():
            if current_time > message_time:
                to_remove.append(message_time)
                broadcast(f"Message from {username} has expired.".encode())
        for message_time in to_remove:
            del message_expiry[message_time]
        time.sleep(60)

def handle_client(client_socket, addr):
    """Handle client requests and messages"""
    client_socket.send("Welcome! Please register or login.".encode())

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                if message.startswith("register"):
                    handle_register(client_socket, message[9:])
                elif message.startswith("login"):
                    handle_login(client_socket, message[6:])
                elif message.startswith("send_msg"):
                    handle_send_message(client_socket, message[9:])
                elif message.startswith("create_group"):
                    group_name = message[13:]
                    create_group(client_socket, group_name)
                elif message.startswith("join_group"):
                    group_name = message[11:]
                    join_group(client_socket, group_name)
                elif message.startswith("expire_message"):
                    expire_message(client_socket, message[15:])
                elif message.startswith("private_msg"):
                    recipient, private_message = message[12:].split(' ', 1)
                    handle_private_message(client_socket, recipient, private_message)
                else:
                    client_socket.send("Invalid command!".encode())
            else:
                break
        except:
            remove_client(client_socket)
            break

def handle_register(client_socket, details):
    """Handle user registration"""
    username, password = details.split(',')
    clients[client_socket] = {'username': username, 'password': password}
    client_socket.send(f"Registered successfully as {username}".encode())

def handle_login(client_socket, details):
    """Handle user login"""
    username, password = details.split(',')
    if client_socket in clients:
        if clients[client_socket]['username'] == username and clients[client_socket]['password'] == password:
            client_socket.send(f"Login successful as {username}".encode())
        else:
            client_socket.send("Invalid credentials.".encode())
    else:
        client_socket.send("Please register first.".encode())

def handle_send_message(client_socket, message):
    """Handle message sending to all clients or specific group"""
    if message.startswith("@"):
        recipient = message[1:message.find(' ')]
        private_message = message[message.find(' ')+1:]
        handle_private_message(client_socket, recipient, private_message)
    else:
        username = clients[client_socket]['username']
        broadcast(f"{username}: {message}", client_socket)

def expire_message(client_socket, time_details):
    """Handle message expiry by user input of date, month, year"""
    try:
        expiry_time = datetime.datetime.strptime(time_details, "%d-%m-%Y %H:%M:%S")
        username = clients[client_socket]['username']
        message_expiry[expiry_time] = username
        client_socket.send(f"Message set to expire at {expiry_time}".encode())
    except:
        client_socket.send("Invalid date format. Use: dd-mm-yyyy HH:MM:SS".encode())

def start_server():
    """Start the server to listen for incoming connections"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 24345))
    server_socket.listen(5)

    print("Server started on 0.0.0.0:24345")

    # Start a thread to remove expired messages periodically
    threading.Thread(target=remove_expired_messages, daemon=True).start()

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection established with {addr}")
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
