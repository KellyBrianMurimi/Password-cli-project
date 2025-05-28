import argparse
from lib.db import session
from lib.models import User, Account, Password
from lib.encryption import encrypt_password, decrypt_password

def create_user(name, email):
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    print(f"User '{name}' created.")

def list_users():
    users = session.query(User).all()
    for user in users:
        print(f"{user.id}: {user.name} ({user.email})")

def delete_user(name):
    user = session.query(User).filter_by(name=name).first()
    if user:
        session.delete(user)
        session.commit()
        print(f"User '{name}' deleted.")
    else:
        print("User not found.")

def add_account(user_name, account_name):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return
    account = Account(name=account_name, user=user)
    session.add(account)
    session.commit()
    print(f"Account '{account_name}' added to user '{user_name}'.")

def list_accounts(user_name):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return
    for account in user.accounts:
        print(f"{account.id}: {account.name}")

def delete_account(user_name, account_name):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return
    account = session.query(Account).filter_by(name=account_name, user_id=user.id).first()
    if account:
        session.delete(account)
        session.commit()
        print(f"Account '{account_name}' deleted.")
    else:
        print("Account not found.")

def add_password(user_name, account_name, password_text):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return
    account = session.query(Account).filter_by(name=account_name, user_id=user.id).first()
    if not account:
        print("Account not found.")
        return
    encrypted_pw = encrypt_password(password_text)
    password = Password(encrypted_password=encrypted_pw, account=account)
    session.add(password)
    session.commit()
    print("Password added successfully.")

def get_passwords(user_name, account_name):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return
    account = session.query(Account).filter_by(name=account_name, user_id=user.id).first()
    if not account:
        print("Account not found.")
        return
    for pw in account.passwords:
        decrypted = decrypt_password(pw.encrypted_password)
        print(f"{pw.id}: {decrypted}")

def delete_password(user_name, account_name, password_id):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return
    account = session.query(Account).filter_by(name=account_name, user_id=user.id).first()
    if not account:
        print("Account not found.")
        return
    password = session.query(Password).filter_by(id=password_id, account_id=account.id).first()
    if password:
        session.delete(password)
        session.commit()
        print(f"Password ID {password_id} deleted.")
    else:
        print("Password not found.")

def update_password(user_name, account_name, password_id, new_password):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return
    account = session.query(Account).filter_by(name=account_name, user_id=user.id).first()
    if not account:
        print("Account not found.")
        return
    password = session.query(Password).filter_by(id=password_id, account_id=account.id).first()
    if password:
        password.encrypted_password = encrypt_password(new_password)
        session.commit()
        print(f"Password ID {password_id} updated.")
    else:
        print("Password not found.")

# --------- CLI ARGUMENTS ---------

parser = argparse.ArgumentParser(description="Password Manager CLI")
subparsers = parser.add_subparsers(dest="command")

# User commands
user_create = subparsers.add_parser("create-user")
user_create.add_argument("name")
user_create.add_argument("email")

user_list = subparsers.add_parser("list-users")

user_delete = subparsers.add_parser("delete-user")
user_delete.add_argument("name")

# Account commands
account_add = subparsers.add_parser("add-account")
account_add.add_argument("user_name")
account_add.add_argument("account_name")

account_list = subparsers.add_parser("list-accounts")
account_list.add_argument("user_name")

account_delete = subparsers.add_parser("delete-account")
account_delete.add_argument("user_name")
account_delete.add_argument("account_name")

# Password commands
pw_add = subparsers.add_parser("add-password")
pw_add.add_argument("user_name")
pw_add.add_argument("account_name")
pw_add.add_argument("password")

pw_get = subparsers.add_parser("get-passwords")
pw_get.add_argument("user_name")
pw_get.add_argument("account_name")

pw_delete = subparsers.add_parser("delete-password")
pw_delete.add_argument("user_name")
pw_delete.add_argument("account_name")
pw_delete.add_argument("password_id", type=int)

pw_update = subparsers.add_parser("update-password")
pw_update.add_argument("user_name")
pw_update.add_argument("account_name")
pw_update.add_argument("password_id", type=int)
pw_update.add_argument("new_password")

# Execute command
args = parser.parse_args()

if args.command == "create-user":
    create_user(args.name, args.email)
elif args.command == "list-users":
    list_users()
elif args.command == "delete-user":
    delete_user(args.name)
elif args.command == "add-account":
    add_account(args.user_name, args.account_name)
elif args.command == "list-accounts":
    list_accounts(args.user_name)
elif args.command == "delete-account":
    delete_account(args.user_name, args.account_name)
elif args.command == "add-password":
    add_password(args.user_name, args.account_name, args.password)
elif args.command == "get-passwords":
    get_passwords(args.user_name, args.account_name)
elif args.command == "delete-password":
    delete_password(args.user_name, args.account_name, args.password_id)
elif args.command == "update-password":
    update_password(args.user_name, args.account_name, args.password_id, args.new_password)
else:
    parser.print_help()
