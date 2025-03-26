from cryptography.fernet import Fernet

# load encryption key
def load_key():
    with open ("secret.key", "rb") as key_file:
        return key_file.read()

# encrypt function
def encrypt_message(message: str) -> bytes:
    cipher = Fernet(load_key())
    return cipher.encrypt(message.encode())

# decrypt function
def decrypt_message(encrypted_message: bytes) -> str:
    cipher = Fernet(load_key())
    return cipher.decrypt(encrypted_message).decode()


message = "Flight data: secure123"
encrypted = encrypt_message(message)
print(f"Encrypted: {encrypted}")

decrypted = decrypt_message(encrypted)
print(f"Decrypted: {decrypted}")