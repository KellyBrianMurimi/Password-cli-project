# 🔐 CLI Password Manager

A secure, lightweight command-line password manager built with Python, SQLAlchemy, Alembic, and Click. Easily manage users, encrypted accounts, and generate strong passwords right from your terminal.

## Project structure
Password-cli-project/
│
├── alembic/                      # Alembic migration system
│   ├── versions/                 # Auto-generated migration scripts
│   └── env.py                    # Alembic environment configuration
│
├── app/
│   ├── __init__.py              # App initialization
│   └── cli.py                   # Main CLI commands using Click
│
├── lib/                         # Core application logic
│   ├── db.py                    # SQLAlchemy DB session setup
│   ├── debug.py                 # Script for interactive testing/debugging
│   ├── encryption.py            # Fernet encryption and password generation
│   └── models/                  # ORM model definitions
│       ├── __init__.py
│       ├── base.py              # SQLAlchemy declarative base
│       ├── account.py           # Account model
│       ├── user.py              # User model
│       └── password.py          # Password model
│
├── helpers.py                   # Utility/helper functions (if applicable)
├── seed.py                      # Seed script for test/demo data
│
├── .env                         # Environment variables (keep secret)
├── .schema                      # Optional schema plan or metadata
├── alembic.ini                  # Alembic configuration file
├── Pipfile                      # Project dependencies
├── Pipfile.lock                 # Locked dependencies
├── securecli.db                 # Local SQLite database
├── README.md                    # 📘 Project documentation

## Setup Instructions
Remove Existing Git Configuration (if using a template)
rm -rf .git .github .canvas
This removes old Git metadata and course-specific files you don’t need.

## Create Your Own Git Repository
Rename your directory:
cd ..
mv python-p3-cli-project-template <your-project-name>
cd <your-project-name>
Initialize a new git repo and commit:

git add --all
git commit -m 'initial commit'

Create a new repo on GitHub and link it:

git remote add origin <github-repo-url>
git push -u origin main

Install Dependencies Using Pipenv
pipenv install sqlalchemy alembic click cryptography
pipenv shell
Add any other needed libraries as your project grows.

## Database Setup and Alembic Migrations
Initialize Alembic (if not already done):

alembic init migrations
Update your alembic.ini to point to your SQLite DB.

In migrations/env.py, replace the metadata line with:

from lib.models.base import Base
target_metadata = Base.metadata

## Create and apply migrations as you build models:

alembic revision --autogenerate -m "create users and accounts"
alembic upgrade head

Seed the database with:
python seed.py

## Running the CLI App
From the root project folder, enter your Pipenv shell (if not already):

pipenv shell

Run the CLI with:
python -m app.cli [COMMAND] [ARGS]

Available Commands & Usage
Note: To check the commands available,run "python -m app.cli --help"

1. Create a new user
python -m app.cli create-user alice alice@example.com
Expected output:
User 'alice' created.

2. List all users
python -m app.cli list-users
Expected output:
Users:
- ID: 3 | alice (alice@example.com)
- ID: 5 | victor (victor@example.com)

3. List accounts for a user by user ID
python -m app.cli list-accounts 3
Expected output:
Accounts for user ID 3:
- Account ID: 7 | Example Account
- Account ID: 8 | Another Account

4. Add a password to an account (prompts securely)
python -m app.cli add-password 7
You will be prompted securely to enter a password or leave blank for auto-generation.

5. Update a password for an account (prompts securely)
python -m app.cli update-password 7
You will be prompted securely to enter a new password or leave blank for auto-generation.

6. Get decrypted password for an account
python -m app.cli get-password 7
Expected output:
Decrypted password for account ID 7: mySecret123!

7. Delete an account by account ID
python -m app.cli delete-account 7

8. Delete a user by user ID (and their related accounts)
python -m app.cli delete-user 3

9. Generate and add a strong password to an account (auto-generated/manually set)
python -m app.cli generate-password 7

10. Debug: Delete all users, accounts, and passwords (clear the database)

python lib/debug.py
Expected:
All users, accounts, and passwords have been deleted.

## Technologies Used
Python3

SQLAlchemy — ORM for database interaction

Alembic — Database migrations management

Click — CLI commands and argument parsing

Cryptography (Fernet) — Encryption/decryption of passwords

SQLite — Local lightweight database

## Project Relationship Structure

User 1 ────< owns >──── * Account 1 ────< has >──── 1 Password
A User can have multiple Accounts.

-Each Account has one Password (encrypted in the database).

-Passwords are securely encrypted/decrypted via Fernet symmetric encryption.

## Resources used:
Click (CLI library)
https://click.palletsprojects.com/en/latest/

SQLAlchemy ORM
https://docs.sqlalchemy.org/en/14/orm/

Alembic Migrations
https://alembic.sqlalchemy.org/en/latest/

Cryptography — Fernet symmetric encryption
https://cryptography.io/en/latest/fernet/

argparse (alternative CLI library)
https://docs.python.org/3/library/argparse.html

## License 
Copyright <2025> <Kelly Brian>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.