from cryptography.fernet import Fernet

# Generate a secret key (this should be done once and stored securely)
secret_key = Fernet.generate_key()

print(secret_key)

# Create a Fernet instance with the secret key
cipher_suite = Fernet(secret_key)

def encrypt_message(message: str) -> str:
    # Encrypt the message
    encrypted_message = cipher_suite.encrypt(message.encode('utf-8'))
    return encrypted_message.decode('utf-8')

def decrypt_message(encrypted_message: str) -> str:
    # Decrypt the message
    decrypted_message = cipher_suite.decrypt(encrypted_message.encode('utf-8'))
    return decrypted_message.decode('utf-8')

# Example usage
message = "This is a secret message"
encrypted = encrypt_message(message)
print(f"Encrypted: {encrypted}")

decrypted = decrypt_message(encrypted)
print(f"Decrypted: {decrypted}")