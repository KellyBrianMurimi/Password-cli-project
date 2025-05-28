import secrets
import string
from cryptography.fernet import Fernet

# WARNING: In a real-world project, store this key securely, not in plain code!
KEY = b'5lozFBg4NaghlzjzA4Pzz5Kd6vwegFieGTGmebpS_cQ='
cipher_suite = Fernet(KEY)

def encrypt_password(plain_text_password):
    """Encrypt the plain text password using Fernet symmetric encryption."""
    return cipher_suite.encrypt(plain_text_password.encode()).decode()

def decrypt_password(encrypted_password):
    """Decrypt the encrypted password."""
    return cipher_suite.decrypt(encrypted_password.encode()).decode()

def generate_strong_password(length=16):
    """Generate a strong random password with letters, digits, and punctuation."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        pwd = ''.join(secrets.choice(alphabet) for _ in range(length))
        if (any(c.islower() for c in pwd) and any(c.isupper() for c in pwd)
                and any(c.isdigit() for c in pwd) and any(c in string.punctuation for c in pwd)):
            return pwd
