# lib/encryption.py
from cryptography.fernet import Fernet

# In real apps, load this from a secure location or environment
key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt_password(password: str) -> str:
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password: str) -> str:
    return cipher.decrypt(encrypted_password.encode()).decode()
