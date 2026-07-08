# Secure Chat Application Using RSA Encryption

## Overview

The **Secure Chat Application Using RSA Encryption** is a Python-based client-server messaging application that enables secure communication between multiple users. The application uses **RSA public-key cryptography** to encrypt private messages so that only the intended recipient can decrypt and read them. Socket programming is used for communication, while multithreading enables multiple clients to communicate simultaneously.

---

## Features

* RSA public and private key generation
* Secure private messaging using RSA encryption
* Public chat between connected users
* Multi-client communication
* Client-server architecture
* Socket programming
* Multithreading for concurrent clients

---

## Project Structure

```text
Source Code/
│── client.py
│── server.py
│── keys.py
```

---

## Requirements

* Python 3.10 or later
* PyCryptodome

---

## Installation

Install the required package:

```bash
pip install pycryptodome
```

or

```bash
pip install -r requirements.txt
```

---

## Source Files

### `keys.py`

Generates a 2048-bit RSA key pair for each user.

Generated files:

* `<username>_private.pem`
* `<username>_public.pem`

### `server.py`

Acts as the central server by:

* Accepting multiple client connections
* Storing usernames and public keys
* Forwarding public and private messages
* Sharing public keys with clients
* Managing communication between users

### `client.py`

Handles client-side communication by:

* Connecting to the server
* Loading RSA keys
* Sending the user's public key
* Encrypting private messages
* Decrypting received private messages

---

# Project Execution

## Step 1: Generate RSA Keys

Run the following command for each user:

```bash
python keys.py
```

Example:

```text
Enter your username: alice
```

This creates:

```text
alice_private.pem
alice_public.pem
```

Repeat the same process for every user (for example, `bob`, `charlie`, etc.).

---

## Step 2: Start the Server

Run:

```bash
python server.py
```

The server starts listening for incoming client connections.

---

## Step 3: Start the Client

Open a new terminal and run:

```bash
python client.py
```

Enter your username when prompted.

Run another instance of `client.py` for each additional user.

---

# Working Procedure

### 1. Key Generation

Each user generates an RSA public and private key pair using `keys.py`.

### 2. Client Connection

When a client starts:

* The client loads the RSA keys.
* Connects to the server.
* Sends the username.
* Sends the user's public key.

### 3. Public Key Storage

The server stores:

* Username
* Client socket
* Public key

This allows other users to request the recipient's public key when sending private messages.

### 4. Public Chat

Users can send normal text messages.

The server broadcasts these messages to every connected client except the sender.

### 5. Private Chat Using RSA

When a user sends a private message:

1. The sender requests the recipient's public key from the server.
2. The server sends the recipient's public key.
3. The sender encrypts the message using the recipient's public key.
4. The encrypted message is sent to the server.
5. The server forwards the encrypted message to the recipient.
6. The recipient decrypts the message using their private key.

Since only the recipient owns the corresponding private key, only they can read the original message.

---

## Communication Flow

```text
Generate RSA Keys
        │
        ▼
Start Server
        │
        ▼
Client Connects
        │
        ▼
Send Username + Public Key
        │
        ▼
Server Stores Public Key
        │
        ▼
Public Chat
        │
        ▼
Private Message
        │
        ▼
Request Recipient Public Key
        │
        ▼
RSA Encryption
        │
        ▼
Encrypted Message
        │
        ▼
Server Forwards Ciphertext
        │
        ▼
Recipient Decrypts Message
```

---

## Technologies Used

* Python
* Socket Programming
* RSA Public-Key Cryptography
* PyCryptodome
* Multithreading

---

## Future Enhancements

* Graphical User Interface (GUI)
* Secure user authentication with a database
* End-to-end encrypted group chat
* File transfer with hybrid RSA-AES encryption
* Message history and logging
* Digital signatures for message authentication

---
