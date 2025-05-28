# lib/seed.py
from lib.db import Session
from lib.models.user import User
from lib.models.account import Account
from lib.models.password import Password
from lib.encryption import encrypt_password

def seed():
    session = Session()

    # Clear existing data (optional, for dev)
    session.query(Password).delete()
    session.query(Account).delete()
    session.query(User).delete()

    # Users
    kelly = User(username="kelly", email="kelly@example.com")
    testuser = User(username="testuser", email="testuser@example.com")

    session.add_all([kelly, testuser])
    session.commit()  # commit to get user ids

    # Accounts - fix: use user_id, account_name, account_type
    github_kelly = Account(user_id=kelly.id, account_name="GitHub", account_type="social")
    gmail_kelly = Account(user_id=kelly.id, account_name="Gmail", account_type="email")
    github_test = Account(user_id=testuser.id, account_name="GitHub", account_type="social")

    session.add_all([github_kelly, gmail_kelly, github_test])
    session.commit()  # commit to get account ids

 # Passwords
    password1 = Password(
    account_id=github_kelly.id,
    encrypted_password=encrypt_password("kellyGitHub123!")
    )
    password2 = Password(
    account_id=gmail_kelly.id,
    encrypted_password=encrypt_password("kellyGmail456!")
   )
    password3 = Password(
    account_id=github_test.id,
    encrypted_password=encrypt_password("testGitHub789!")
   )

    session.add_all([password1, password2, password3])
    session.commit()
    session.close()
    print("✅ Database seeded with test users, accounts, and passwords.")

if __name__ == "__main__":
    seed()
