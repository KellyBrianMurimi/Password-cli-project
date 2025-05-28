# lib/seed.py
from lib.db import Session
from lib.models.user import User
from lib.models.account import Account
from lib.models.password import Password
from lib.encryption import encrypt_password
from datetime import datetime

def seed():
    session = Session()

    # Create user
    user1 = User(username="testuser", email="testuser@example.com")
    
    # Create account for that user
    account1 = Account(name="GitHub", user=user1)
    
    # Encrypt the password
    encrypted_pw = encrypt_password("MyStrongPassword123!")

    # Create password record linked to account and user (if your model has user relation)
    password1 = Password(
        account=account1,
        user=user1,
        encrypted_value=encrypted_pw,
    )

    # Add all records and commit
    session.add_all([user1, account1, password1])
    session.commit()
    session.close()
    
    print("✅ Database seeded successfully.")

if __name__ == "__main__":
    seed()
