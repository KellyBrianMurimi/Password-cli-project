# cli.py
import argparse
from lib.db import Session
from lib.models.user import User
from lib.models.account import Account
from lib.models.password import Password
from lib.encryption import encrypt_password, decrypt_password  # assuming decrypt exists
from datetime import datetime

def list_accounts(username):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if not user:
        print(f"User '{username}' not found.")
        session.close()
        return
    print(f"Accounts for user '{username}':")
    for account in user.accounts:
        print(f"- {account.name} (ID: {account.id})")
    session.close()

def add_account(username, account_name):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if not user:
        print(f"User '{username}' not found.")
        session.close()
        return
    account = Account(name=account_name, user=user)
    session.add(account)
    session.commit()
    print(f"Account '{account_name}' added for user '{username}'.")
    session.close()

def add_password(username, account_name, password_plain):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if not user:
        print(f"User '{username}' not found.")
        session.close()
        return
    account = session.query(Account).filter_by(name=account_name, user=user).first()
    if not account:
        print(f"Account '{account_name}' not found for user '{username}'.")
        session.close()
        return
    encrypted_pw = encrypt_password(password_plain)
    pw_entry = Password(
        account=account,
        user=user,
        encrypted_value=encrypted_pw,
        created_at=datetime.utcnow()
    )
    session.add(pw_entry)
    session.commit()
    print(f"Password added for account '{account_name}'.")
    session.close()

def get_passwords(username, account_name):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if not user:
        print(f"User '{username}' not found.")
        session.close()
        return
    account = session.query(Account).filter_by(name=account_name, user=user).first()
    if not account:
        print(f"Account '{account_name}' not found for user '{username}'.")
        session.close()
        return
    pw_entries = session.query(Password).filter_by(account=account).all()
    if not pw_entries:
        print(f"No passwords found for account '{account_name}'.")
    else:
        print(f"Passwords for account '{account_name}':")
        for pw in pw_entries:
            decrypted = decrypt_password(pw.encrypted_value)
            print(f"- Created at {pw.created_at}: {decrypted}")
    session.close()

def main():
    parser = argparse.ArgumentParser(description="Password Manager CLI")
    subparsers = parser.add_subparsers(dest="command")

    # List accounts
    parser_list = subparsers.add_parser("list-accounts")
    parser_list.add_argument("username", help="Username to list accounts for")

    # Add account
    parser_add_acc = subparsers.add_parser("add-account")
    parser_add_acc.add_argument("username", help="Username to add account for")
    parser_add_acc.add_argument("account_name", help="Name of the new account")

    # Add password
    parser_add_pw = subparsers.add_parser("add-password")
    parser_add_pw.add_argument("username", help="Username for the account")
    parser_add_pw.add_argument("account_name", help="Account name")
    parser_add_pw.add_argument("password", help="Password to add")

    # Get passwords
    parser_get_pw = subparsers.add_parser("get-passwords")
    parser_get_pw.add_argument("username", help="Username for the account")
    parser_get_pw.add_argument("account_name", help="Account name")

    args = parser.parse_args()

    if args.command == "list-accounts":
        list_accounts(args.username)
    elif args.command == "add-account":
        add_account(args.username, args.account_name)
    elif args.command == "add-password":
        add_password(args.username, args.account_name, args.password)
    elif args.command == "get-passwords":
        get_passwords(args.username, args.account_name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
