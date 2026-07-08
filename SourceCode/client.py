import socket
import threading
import os

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

HOST = "127.0.0.1"
PORT = 12345


# -----------------------------
# RSA Key Functions
# -----------------------------
def generate_keys(username):
    if os.path.exists(f"{username}_private.pem") and os.path.exists(f"{username}_public.pem"):
        return

    key = RSA.generate(2048)

    with open(f"{username}_private.pem", "wb") as f:
        f.write(key.export_key())

    with open(f"{username}_public.pem", "wb") as f:
        f.write(key.publickey().export_key())

    print("RSA keys generated.")


def load_private(username):
    with open(f"{username}_private.pem", "rb") as f:
        return RSA.import_key(f.read())


def load_public(username):
    with open(f"{username}_public.pem", "rb") as f:
        return RSA.import_key(f.read())


# -----------------------------
# Receive Thread
# -----------------------------
def receive_messages(sock, private_key):
    cipher = PKCS1_OAEP.new(private_key)

    while True:
        try:
            data = sock.recv(8192)

            if not data:
                break

            if data.startswith(b"PRIVATE_FROM:"):

                parts = data.split(b":", 2)

                sender = parts[1].decode()
                encrypted = parts[2]

                try:
                    message = cipher.decrypt(encrypted).decode()
                    print(f"\n[PRIVATE] {sender}: {message}")
                except Exception:
                    print("\nFailed to decrypt message.")

            else:
                print(data.decode())

        except:
            break


# -----------------------------
# Main
# -----------------------------
username = input("Username: ")

generate_keys(username)

private_key = load_private(username)
public_key = load_public(username)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Send username
sock.send(username.encode())

# Send public key
sock.send(public_key.export_key())

threading.Thread(
    target=receive_messages,
    args=(sock, private_key),
    daemon=True
).start()

print("\nCommands")
print("-------------------------------------")
print("@username message  -> Private RSA message")
print("message            -> Public message")
print("exit               -> Quit")
print("-------------------------------------")

while True:

    msg = input("> ")

    if msg.lower() == "exit":
        break

    # ----------------------------
    # RSA Private Message
    # ----------------------------
    if msg.startswith("@"):

        try:
            recipient = msg.split(" ")[0][1:]
            message = msg.split(" ", 1)[1]

            # Request recipient public key
            sock.send(f"GET_KEY:{recipient}".encode())

            status = sock.recv(1024)

            if status == b"KEY_NOT_FOUND":
                print("User not found.")
                continue

            key_data = sock.recv(4096)

            recipient_key = RSA.import_key(key_data)

            cipher = PKCS1_OAEP.new(recipient_key)

            encrypted = cipher.encrypt(message.encode())

            packet = (
                b"PRIVATE:"
                + recipient.encode()
                + b":"
                + encrypted
            )

            sock.send(packet)

        except Exception as e:
            print("Error:", e)

    # ----------------------------
    # Public Message
    # ----------------------------
    else:
        sock.send(msg.encode())

sock.close()
