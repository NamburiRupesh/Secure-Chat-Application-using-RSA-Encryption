import socket
import threading

# username -> socket
client_sockets = {}

# username -> public key (bytes)
client_public_keys = {}


def handle_client(client_socket):
    username = None

    try:
        # Receive username
        username = client_socket.recv(1024).decode()

        # Receive public key
        public_key = client_socket.recv(4096)

        client_sockets[username] = client_socket
        client_public_keys[username] = public_key

        print(f"{username} joined the chat.")

        while True:

            data = client_socket.recv(8192)

            if not data:
                break

            text = data.decode(errors="ignore")

            # -------------------------
            # Client requesting a public key
            # -------------------------
            if text.startswith("GET_KEY:"):

                target = text.split(":")[1]

                if target in client_public_keys:

                    client_socket.send(b"KEY_FOUND")
                    client_socket.send(client_public_keys[target])

                else:

                    client_socket.send(b"KEY_NOT_FOUND")

            # -------------------------
            # RSA encrypted private message
            # -------------------------
            elif text.startswith("PRIVATE:"):

                parts = data.split(b":", 2)

                recipient = parts[1].decode()

                encrypted_message = parts[2]

                if recipient in client_sockets:

                    client_sockets[recipient].send(
                        b"PRIVATE_FROM:" +
                        username.encode() +
                        b":" +
                        encrypted_message
                    )

                else:

                    client_socket.send(b"User not found.")

            # -------------------------
            # Normal broadcast message
            # -------------------------
            else:

                for user, sock in client_sockets.items():

                    if user != username:

                        sock.send(f"{username}: {text}".encode())

    except Exception as e:

        print("Error:", e)

    finally:

        if username:

            client_sockets.pop(username, None)
            client_public_keys.pop(username, None)

            print(f"{username} disconnected.")

        client_socket.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("0.0.0.0", 12345))

server.listen(5)

print("RSA Secure Chat Server Running on Port 12345...")

while True:

    conn, addr = server.accept()

    print("Connected:", addr)

    threading.Thread(
        target=handle_client,
        args=(conn,),
        daemon=True
    ).start()
