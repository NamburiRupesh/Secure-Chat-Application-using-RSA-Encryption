import os
from Crypto.PublicKey import RSA

# Function to load keys
def load_keys(username):
    private_key_file = f"{username}_private.pem"
    public_key_file = f"{username}_public.pem"
    
    # Check if the keys exist
    if not os.path.exists(private_key_file) or not os.path.exists(public_key_file):
        print(f"Keys not found for {username}, generating new keys...")
        generate_keys(username)
    
    # Load private and public keys from files
    try:
        print(f"Attempting to load keys from: {os.path.abspath(private_key_file)} and {os.path.abspath(public_key_file)}")
        with open(private_key_file, 'rb') as priv_file:
            private_key = RSA.import_key(priv_file.read())
        with open(public_key_file, 'rb') as pub_file:
            public_key = RSA.import_key(pub_file.read())
        print("Keys loaded successfully!")
        return private_key, public_key
    except Exception as e:
        print(f"Error loading keys: {e}")
        return None, None

# Function to generate RSA keys
def generate_keys(username):
    private_key_file = f"{username}_private.pem"
    public_key_file = f"{username}_public.pem"
    
    # Check if keys already exist
    if os.path.exists(private_key_file) and os.path.exists(public_key_file):
        print(f"Keys already exist for {username}.")
        return
    
    # Generate RSA key pair (2048 bits)
    print("Generating RSA key pair...")
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    # Save the private key
    with open(private_key_file, "wb") as priv_file:
        priv_file.write(private_key)
    print(f"Private key saved to {os.path.abspath(private_key_file)}")

    # Save the public key
    with open(public_key_file, "wb") as pub_file:
        pub_file.write(public_key)
    print(f"Public key saved to {os.path.abspath(public_key_file)}")

    print(f"Keys generated successfully for {username}!")

# Example usage of the load_keys function
if __name__ == "__main__":
    username = input("Enter your username: ")
    private_key, public_key = load_keys(username)
    if private_key and public_key:
        # Use the keys for further operations, like encrypting/decrypting messages
        pass
