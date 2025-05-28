import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

FERNET_KEY = os.getenv("FERNET_KEY")

if not FERNET_KEY:
    raise ValueError("FERNET_KEY not found in environment variables!")

cipher = Fernet(FERNET_KEY)

def encrypt_password(password):
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()
