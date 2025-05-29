import os
import click
from getpass import getpass
from lib.db import Session
from lib.models import User, Account, Password
from lib.encryption import encrypt_password, decrypt_password, generate_strong_password

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///securecli.db")
print(f"Using database: {DATABASE_URL}")

@click.group()
def cli():
    """Password Manager CLI — Manage users, accounts, and passwords securely."""
    pass

@cli.command()
@click.argument('username')
@click.argument('email')
def create_user(username, email):
    """Create a new user with USERNAME and EMAIL."""
    session = Session()
    user = User(username=username, email=email)
    session.add(user)
    session.commit()
    click.echo(f"User '{username}' created successfully.")
    session.close()

@cli.command()
def list_users():
    """List all users."""
    session = Session()
    users = session.query(User).all()
    if not users:
        click.echo("No users found.")
    else:
        click.echo("Users:")
        for user in users:
            click.echo(f"- ID: {user.id} | {user.username} ({user.email})")
    session.close()

@cli.command()
@click.argument('user_id', type=int)
@click.argument('site')
@click.argument('username')
def create_account(user_id, site, username):
    """Create an account for USER_ID with SITE and USERNAME."""
    session = Session()
    user = session.query(User).get(user_id)
    if not user:
        click.echo(f"User with ID {user_id} does not exist.")
        session.close()
        return
    account = Account(site=site, username=username, user=user)
    session.add(account)
    session.commit()
    click.echo(f"Account for '{site}' created successfully with ID: {account.id}.")
    session.close()

@cli.command()
@click.argument('user_id', type=int)
def list_accounts(user_id):
    """List all accounts for USER_ID."""
    session = Session()
    user = session.query(User).get(user_id)
    if not user:
        click.echo(f"User with ID {user_id} does not exist.")
        session.close()
        return
    if not user.accounts:
        click.echo("No accounts found for this user.")
    else:
        click.echo(f"Accounts for {user.username}:")
        for account in user.accounts:
            click.echo(f"- ID: {account.id} | Site: {account.site} | Username: {account.username}")
    session.close()

@cli.command()
@click.argument('account_id', type=int)
def add_password(account_id):
    """Add an encrypted password to ACCOUNT_ID."""
    session = Session()
    account = session.query(Account).get(account_id)
    if not account:
        click.echo(f"Account with ID {account_id} does not exist.")
        session.close()
        return
    # Secure password prompt
    password = getpass("Enter password to encrypt (leave blank to auto-generate): ").strip()
    if not password:
        password = generate_strong_password()
        click.echo("Generated strong password.")
    encrypted = encrypt_password(password)
    pwd = Password(encrypted_password=encrypted, account=account)
    session.add(pwd)
    session.commit()
    click.echo("Password added successfully.")
    session.close()

@cli.command()
@click.argument('account_id', type=int)
def get_password(account_id):
    """Retrieve and decrypt a password for ACCOUNT_ID."""
    session = Session()
    account = session.query(Account).get(account_id)
    if not account or not account.passwords:
        click.echo("No password found for this account.")
        session.close()
        return
    password = account.passwords[0]  # Assuming 1 password per account
    decrypted = decrypt_password(password.encrypted_password)
    click.echo(f"Decrypted password: {decrypted}")
    session.close()

@cli.command()
@click.argument('account_id', type=int)
def generate_password(account_id):
    """Generate a strong password for ACCOUNT_ID and store it."""
    session = Session()
    account = session.query(Account).get(account_id)
    if not account:
        click.echo(f"Account with ID {account_id} does not exist.")
        session.close()
        return
    strong_pwd = generate_strong_password()
    encrypted = encrypt_password(strong_pwd)
    pwd = Password(encrypted_password=encrypted, account=account)
    session.add(pwd)
    session.commit()
    click.echo(f"Generated password stored for account ID {account_id}: {strong_pwd}")
    session.close()

@cli.command()
@click.argument('user_id', type=int)
def delete_user(user_id):
    """Delete user by USER_ID (will delete related accounts and passwords)."""
    session = Session()
    user = session.query(User).get(user_id)
    if not user:
        click.echo(f"User with ID {user_id} not found.")
    else:
        confirm = click.confirm(f"Are you sure you want to delete user '{user.username}' and all related data?", default=False)
        if confirm:
            session.delete(user)
            session.commit()
            click.echo("User deleted.")
    session.close()

@cli.command()
@click.argument('account_id', type=int)
def delete_account(account_id):
    """Delete account by ACCOUNT_ID."""
    session = Session()
    account = session.query(Account).get(account_id)
    if not account:
        click.echo(f"Account with ID {account_id} not found.")
    else:
        confirm = click.confirm(f"Are you sure you want to delete account for '{account.site}'?", default=False)
        if confirm:
            session.delete(account)
            session.commit()
            click.echo("Account deleted.")
    session.close()

@cli.command()
@click.argument('account_id', type=int)
def update_password(account_id):
    """Update the password for ACCOUNT_ID."""
    session = Session()
    account = session.query(Account).get(account_id)
    if not account or not account.passwords:
        click.echo("Account or password not found.")
        session.close()
        return
    new_password = getpass("Enter new password (leave blank to auto-generate): ").strip()
    if not new_password:
        new_password = generate_strong_password()
        click.echo("Generated strong password.")
    password = account.passwords[0]
    password.encrypted_password = encrypt_password(new_password)
    session.commit()
    click.echo("Password updated successfully.")
    session.close()

@cli.command()
@click.argument('query')
def search_accounts(query):
    """Search accounts by site or username."""
    session = Session()
    results = session.query(Account).filter(
        (Account.site.ilike(f"%{query}%")) |
        (Account.username.ilike(f"%{query}%"))
    ).all()
    if not results:
        click.echo("No matching accounts found.")
    else:
        for acc in results:
            click.echo(f"- ID: {acc.id} | Site: {acc.site} | Username: {acc.username} | User ID: {acc.user_id}")
    session.close()

if __name__ == '__main__':
    cli()
