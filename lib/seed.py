# lib/seed.py
from lib.db import Session
from lib.models.user import User
from lib.models.account import Account
from lib.models.password import Password
from lib.encryption import encrypt_password
from datetime import datetime

def seed():
    session = Session()

    # Clear existing data (optional, for dev)
    session.query(Password).delete()
    session.query(Account).delete()
    session.query(User).delete()

    # Users
    kelly = User(username="kelly", email="kelly@example.com")
    testuser = User(username="testuser", email="testuser@example.com")

    # Accounts
    github_kelly = Account(name="GitHub", user=kelly)
    gmail_kelly = Account(name="Gmail", user=kelly)
    github_test = Account(name="Gmail", user=testuser)

    # Passwords
    password1 = Password(
        account=github_kelly, 
        user=kelly, 
        encrypted_value=encrypt_password("kellyGitHub123!"),
        )
    password2 = Password(
        account=gmail_kelly, 
        user=kelly, encrypted_value=encrypt_password("kellyGmail456!"), 
        )
    password3 = Password(
        account=github_test, 
        user=testuser, encrypted_value=encrypt_password("testGitHub789!"), 
        )

    session.add_all([kelly, testuser, github_kelly, gmail_kelly, github_test, password1, password2, password3])
    session.commit()
    session.close()
    print("✅ Database seeded with test users, accounts, and passwords.")

if __name__ == "__main__":
    seed()
