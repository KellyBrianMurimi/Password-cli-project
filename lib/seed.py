from lib.db import Session
from lib.models.user import User
from lib.models.account import Account
from lib.models.password import Password
from lib.encryption import encrypt_password

def seed():
    session = Session()
    print(f"Using database: {session.bind.url}")

    # Clear existing data
    session.query(Password).delete()
    session.query(Account).delete()
    session.query(User).delete()
    session.commit()

    # Create Users
    kelly = User(username="kellybrian", email="kellybrianmurimi@gmail.com")
    session.add(kelly)
    session.commit()

    # Accounts linked to User (pass user instance, per your Account __init__)
    github_kelly = Account(site="GitHub", username="kellybrianmurimi", user=kelly)
    twitter_kelly = Account(site="Twitter", username="kellymurimi", user=kelly)
    session.add_all([github_kelly, twitter_kelly])
    session.commit()

    # Passwords with encrypted password strings
    pw_github = Password(encrypted_password=encrypt_password("my_real_github_password"), account=github_kelly)
    pw_twitter = Password(encrypted_password=encrypt_password("my_real_twitter_password"), account=twitter_kelly)
    session.add_all([pw_github, pw_twitter])
    session.commit()

    print("Seed data created successfully!")
    session.close()

if __name__ == "__main__":
    seed()
