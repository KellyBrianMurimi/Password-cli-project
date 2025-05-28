# lib/seed.py
from lib.db import Session
from lib.models.user import User
from lib.models.account import Account
from lib.models.password import Password
from lib.encryption import encrypt_password

def seed():
    session = Session()

    # Create user
    user1 = User(username="kelly", email="kelly@example.com")
    
    # Create account
    account1 = Account(name="GitHub", user=user1)
    
    # Create password (encrypted)
    encrypted_pw = encrypt_password("MyStrongPassword123!")
    password1 = Password(account=account1, user=user1, encrypted_value=encrypted_pw)


    session.add_all([user1, account1, password1])
    session.commit()
    session.close()
    print("✅ Database seeded successfully.")

if __name__ == "__main__":
    seed()
