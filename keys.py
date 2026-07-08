from Crypto.PublicKey import RSA
import os

def generate_keys(username):
    private_key_file = f"{username}_private.pem"
    public_key_file = f"{username}_public.pem"
    
    # Check if keys already exist
    if os.path.exists(private_key_file) and os.path.exists(public_key_file):
        print(f"Keys already exist for {username}.")
        return
    
    # Generate RSA key pair (2048 bits)
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    # Save the private key
    with open(private_key_file, "wb") as priv_file:
        priv_file.write(private_key)

    # Save the public key
    with open(public_key_file, "wb") as pub_file:
        pub_file.write(public_key)

    print(f"Keys generated successfully for {username}!")

if __name__ == "__main__":
    username = input("Enter your username: ")
    generate_keys(username)
