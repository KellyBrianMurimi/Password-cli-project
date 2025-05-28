# cli.py
import argparse
from datetime import datetime
from lib.db import Session
from lib.models.user import User
from lib.models.account import Account
from lib.models.password import Password
from lib.encryption import encrypt_password

try:
    from lib.encryption import decrypt_password
except ImportError:
    decrypt_password = lambda val: "[DECRYPTION DISABLED]"

def list_accounts(username):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if not user:
        print(f" User '{username}' not found.")
        session.close()
        return
    print(f" Accounts for user '{username}':")
    for account in user.accounts:
        print(f"- {account.name} (ID: {account.id})")
    session.close()

def add_account(username, account_name):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if not user:
        print(f" User '{username}' not found.")
        session.close()
        return
    account = Account(name=account_name, user=user)
    session.add(account)
    session.commit()
    print(f" Account '{account_name}' added for user '{username}'.")
    session.close()

def add_password(username, account_name, password_plain):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if not user:
        print(f" User '{username}' not found.")
        session.close()
        return
    account = session.query(Account).filter_by(name=account_name, user=user).first()
    if not account:
        print(f" Account '{account_name}' not found for user '{username}'.")
        session.close()
        return
    encrypted_pw = encrypt_password(password_plain)
    pw_entry = Password(
        account=account,
        user=user,
        encrypted_value=encrypted_pw,
    )
    session.add(pw_entry)
    session.commit()
    print(f" Password added for account '{account_name}'.")
    session.close()

def get_passwords(username, account_name):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if not user:
        print(f" User '{username}' not found.")
        session.close()
        return
    account = session.query(Account).filter_by(name=account_name, user=user).first()
    if not account:
        print(f" Account '{account_name}' not found for user '{username}'.")
        session.close()
        return
    pw_entries = session.query(Password).filter_by(account=account).all()
    if not pw_entries:
        print(f" No passwords found for account '{account_name}'.")
    else:
        print(f" Passwords for '{account_name}':")
        for pw in pw_entries:
            decrypted = decrypt_password(pw.encrypted_value)
            print(f"- ID {pw.id}, created {pw.created_at}: {decrypted}")
    session.close()

def create_user(username, email):
    session = Session()
    existing = session.query(User).filter_by(username=username).first()
    if existing:
        print(f"User '{username}' already exists.")
    else:
        new_user = User(username=username, email=email)
        session.add(new_user)
        session.commit()
        print(f" User '{username}' created.")
    session.close()

def update_password(password_id, new_password):
    session = Session()
    pw_entry = session.query(Password).filter_by(id=password_id).first()
    if not pw_entry:
        print(f" Password entry with ID '{password_id}' not found.")
        session.close()
        return
    pw_entry.encrypted_value = encrypt_password(new_password)
    session.commit()
    print(f" Password ID {password_id} updated successfully.")
    session.close()

def delete_password(password_id):
    session = Session()
    pw_entry = session.query(Password).filter_by(id=password_id).first()
    if not pw_entry:
        print(f" Password entry with ID '{password_id}' not found.")
        session.close()
        return
    session.delete(pw_entry)
    session.commit()
    print(f" Password ID {password_id} deleted.")
    session.close()

def main():
    parser = argparse.ArgumentParser(description=" Password Manager CLI")
    subparsers = parser.add_subparsers(dest="command")

    # list-accounts
    parser_list = subparsers.add_parser("list-accounts")
    parser_list.add_argument("username")

    # add-account
    parser_add_acc = subparsers.add_parser("add-account")
    parser_add_acc.add_argument("username")
    parser_add_acc.add_argument("account_name")

    # add-password
    parser_add_pw = subparsers.add_parser("add-password")
    parser_add_pw.add_argument("username")
    parser_add_pw.add_argument("account_name")
    parser_add_pw.add_argument("password")

    # get-passwords
    parser_get_pw = subparsers.add_parser("get-passwords")
    parser_get_pw.add_argument("username")
    parser_get_pw.add_argument("account_name")

    # Create user
    parser_create_user = subparsers.add_parser("create-user")
    parser_create_user.add_argument("username", help="New user's username")
    parser_create_user.add_argument("email", help="New user's email")

    # update-password
    parser_update = subparsers.add_parser("update-password")
    parser_update.add_argument("password_id", type=int)
    parser_update.add_argument("new_password")

    # delete-password
    parser_delete = subparsers.add_parser("delete-password")
    parser_delete.add_argument("password_id", type=int)

    args = parser.parse_args()

    if args.command == "list-accounts":
        list_accounts(args.username)
    elif args.command == "add-account":
        add_account(args.username, args.account_name)
    elif args.command == "add-password":
        add_password(args.username, args.account_name, args.password)
    elif args.command == "get-passwords":
        get_passwords(args.username, args.account_name)
    elif args.command == "create-user":
        create_user(args.username, args.email)
    elif args.command == "update-password":
        update_password(args.password_id, args.new_password)
    elif args.command == "delete-password":
        delete_password(args.password_id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
