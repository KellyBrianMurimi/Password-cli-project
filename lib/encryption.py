import os
import string
import secrets
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# Load environment variables from .env file
load_dotenv()

FERNET_KEY = os.getenv("FERNET_KEY")
if not FERNET_KEY:
    raise ValueError("FERNET_KEY not found in environment variables. Please add it to your .env file.")

fernet = Fernet(FERNET_KEY)

def encrypt_password(password: str) -> str:
    """Encrypt a plaintext password using Fernet symmetric encryption."""
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password: str) -> str:
    """Decrypt an encrypted password back to plaintext."""
    return fernet.decrypt(encrypted_password.encode()).decode()

def generate_strong_password(length: int = 16) -> str:
    """Generate a strong random password with letters, digits, and punctuation."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password
