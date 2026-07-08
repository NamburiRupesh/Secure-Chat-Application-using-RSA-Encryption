# Secure Chat Application Using RSA Encryption

## Description
This project is a secure client-server chat application developed using Python. It uses RSA encryption to provide secure private messaging between users. The application also supports public chat using socket programming and multithreading.

## Features
- User authentication
- RSA key generation
- Secure private messaging using RSA
- Public chat
- Multi-client support
- Socket programming
- Multithreading

## Requirements
- Python 3.10 or above
- PyCryptodome

## Installation

Install the required package:

```bash
pip install pycryptodome
```

## Files

- `server.py` – Starts the chat server.
- `client.py` – Starts the chat client.
- `keys.py` – Generates RSA public and private keys.

## Running the Project

### Step 1: Generate RSA Keys

```bash
python keys.py
```

### Step 2: Start the Server

```bash
python server.py
```

### Step 3: Start the Client

```bash
python client.py
```

Run multiple instances of `client.py` to connect multiple users.

## Project Workflow

1. Generate RSA key pairs.
2. Start the server.
3. Connect clients.
4. Exchange public keys.
5. Encrypt private messages using the recipient's public key.
6. Decrypt messages using the recipient's private key.

## Technologies Used

- Python
- Socket Programming
- RSA Encryption
- Multithreading
- PyCryptodome

## Authors

Group Project
