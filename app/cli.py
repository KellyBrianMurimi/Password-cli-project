import click
from lib.db import Session
from lib.models import User, Account, Password
from lib.crypto import encrypt_password, decrypt_password, generate_strong_password  # imported here

@click.group()
@click.option('-m', '--message', help='Optional operation message')
@click.pass_context
def cli(ctx, message):
    """Main CLI group with optional message for commands."""
    ctx.ensure_object(dict)
    ctx.obj['message'] = message
    click.echo(f"Using database: {Session.kw.get('bind').url}")

@cli.command()
@click.argument('username')
@click.argument('email')
@click.pass_context
def create_user(ctx, username, email):
    """Create a new user."""
    with Session() as session:
        user = User(username=username, email=email)
        session.add(user)
        session.commit()
        click.echo(f"User '{username}' created.")
        if ctx.obj['message']:
            click.echo(f"Message: {ctx.obj['message']}")

@cli.command()
@click.pass_context
def list_users(ctx):
    """List all users."""
    with Session() as session:
        users = session.query(User).all()
        if not users:
            click.echo("No users found.")
            return
        click.echo("Users:")
        for u in users:
            click.echo(f"- ID: {u.id} | {u.username} ({u.email})")
        if ctx.obj['message']:
            click.echo(f"Message: {ctx.obj['message']}")

@cli.command()
@click.argument('user_id', type=int)
@click.argument('site')
@click.argument('username')
@click.pass_context
def add_account(ctx, user_id, site, username):
    """Add an account to a user."""
    with Session() as session:
        user = session.get(User, user_id)
        if not user:
            click.echo(f"Error: User with ID {user_id} does not exist.")
            return
        account = Account(site=site, username=username, user=user)
        session.add(account)
        session.commit()
        click.echo(f"Account for site '{site}' added for user '{user.username}'.")
        if ctx.obj['message']:
            click.echo(f"Message: {ctx.obj['message']}")

@cli.command()
@click.argument('user_id', type=int)
@click.pass_context
def list_accounts(ctx, user_id):
    """List all accounts for a user."""
    with Session() as session:
        user = session.get(User, user_id)
        if not user:
            click.echo(f"Error: User with ID {user_id} not found.")
            return
        accounts = session.query(Account).filter_by(user_id=user_id).all()
        if not accounts:
            click.echo(f"No accounts found for user '{user.username}'.")
            return
        click.echo(f"Accounts for user '{user.username}':")
        for a in accounts:
            click.echo(f"- ID: {a.id} | Site: {a.site} | Username: {a.username}")
        if ctx.obj['message']:
            click.echo(f"Message: {ctx.obj['message']}")

@cli.command()
@click.argument('account_id', type=int)
@click.argument('password_text')
@click.pass_context
def add_password(ctx, account_id, password_text):
    """Add a password (encrypted) to an account."""
    with Session() as session:
        account = session.get(Account, account_id)
        if not account:
            click.echo(f"Error: Account with ID {account_id} not found.")
            return
        encrypted = encrypt_password(password_text)
        password = Password(account_id=account_id, encrypted_password=encrypted)
        session.add(password)
        session.commit()
        click.echo(f"Password added for account ID {account_id}.")
        if ctx.obj['message']:
            click.echo(f"Message: {ctx.obj['message']}")

@cli.command()
@click.argument('account_id', type=int)
@click.pass_context
def generate_and_add_password(ctx, account_id):
    """Generate a strong password, encrypt it, and add it to an account."""
    with Session() as session:
        account = session.get(Account, account_id)
        if not account:
            click.echo(f"Error: Account with ID {account_id} not found.")
            return
        pwd = generate_strong_password()
        encrypted = encrypt_password(pwd)
        password = Password(account_id=account_id, encrypted_password=encrypted)
        session.add(password)
        session.commit()
        click.echo(f"Generated and added password for account ID {account_id}:")
        click.echo(f"{pwd}  <-- Save this password securely!")
        if ctx.obj['message']:
            click.echo(f"Message: {ctx.obj['message']}")

@cli.command()
@click.argument('account_id', type=int)
@click.pass_context
def get_password(ctx, account_id):
    """Retrieve and decrypt a password for an account."""
    with Session() as session:
        password = session.query(Password).filter_by(account_id=account_id).first()
        if not password:
            click.echo(f"No password found for account ID {account_id}.")
            return
        decrypted = decrypt_password(password.encrypted_password)
        click.echo(f"Decrypted password for account ID {account_id}: {decrypted}")
        if ctx.obj['message']:
            click.echo(f"Message: {ctx.obj['message']}")

@cli.command()
@click.argument('password_id', type=int)
@click.pass_context
def delete_password(ctx, password_id):
    """Delete a password by ID."""
    with Session() as session:
        password = session.get(Password, password_id)
        if not password:
            click.echo(f"Password with ID {password_id} not found.")
            return
        session.delete(password)
        session.commit()
        click.echo(f"Password ID {password_id} deleted.")
        if ctx.obj['message']:
            click.echo(f"Message: {ctx.obj['message']}")

@cli.command()
@click.argument('account_id', type=int)
@click.pass_context
def delete_account(ctx, account_id):
    """Delete an account by ID."""
    with Session() as session:
        account = session.get(Account, account_id)
        if not account:
            click.echo(f"Account with ID {account_id} not found.")
            return
        session.delete(account)
        session.commit()
        click.echo(f"Account ID {account_id} deleted.")
        if ctx.obj['message']:
            click.echo(f"Message: {ctx.obj['message']}")

@cli.command()
@click.argument('user_id', type=int)
@click.pass_context
def delete_user(ctx, user_id):
    """Delete a user by ID."""
    with Session() as session:
        user = session.get(User, user_id)
        if not user:
            click.echo(f"User with ID {user_id} not found.")
            return
        session.delete(user)
        session.commit()
        click.echo(f"User ID {user_id} deleted.")
        if ctx.obj['message']:
            click.echo(f"Message: {ctx.obj['message']}")

if __name__ == '__main__':
    cli()
