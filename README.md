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

## Setup instructions

-Removing Existing Git Configuration

If you're using this template, start off by removing the existing metadata for
Github and Canvas. Run the following command to carry this out:

```console
$ rm -rf .git .github .canvas
```

The `rm` command removes files from your computer's memory. The `-r` flag tells
the console to remove _recursively_, which allows the command to remove
directories and the files within them. `-f` removes them permanently.

`.git` contains this directory's configuration to track changes and push to
Github (you want to track and push _your own_ changes instead), and `.github`
and `.canvas` contain the metadata to create a Canvas page from your Git repo.
You don't have the permissions to edit our Canvas course, so it's not worth
keeping them around.

-Creating Your Own Git Repo

First things first- rename this directory! Once you have an idea for a name,
move one level up with `cd ..` and run `mv python-p3-cli-project-template
<new-directory-name>` to change its name.

> **Note: `mv` actually stands for "move", but your computer interprets this
> rename as a move from a directory with the old name to a directory with
> a new name.**

`cd` back into your new directory and run `git init` to create a local git
repository. Add all of your local files to version control with `git add --all`,
then commit them with `git commit -m'initial commit'`. (You can change the
message here- this one is just a common choice.)

Navigate to [GitHub](https://github.com). In the upper-right corner of the page,
click on the "+" dropdown menu, then select "New repository". Enter the name of
your local repo, choose whether you would like it to be public or private, make
sure "Initialize this repository with a README" is unchecked (you already have
one), then click "Create repository".

Head back to the command line and enter `git remote add <project name> <github
url>`. This will map the remote repository to your local repository. Finally,
push your first commit with `git push -u origin main`.

Your project is now version-controlled locally and online. This will allow you
to create different versions of your project and pick up your work on a
different machine if the need arises.

-Generating Your Pipenv

You might have noticed in the file structure- there's already a Pipfile! That
being said, we haven't put much in there- just Python version 3.8 and ipdb.

Install any dependencies you know you'll need for your project, like SQLAlchemy
and Alembic, before you begin. You can do this straight from the command line:

```console
$ pipenv install sqlalchemy alembic
```

From here, you should run your second commit:

```console
$ git add Pipfile Pipfile.lock
$ git commit -m'add sqlalchemy and alembic to pipenv'
$ git push
```

Now that your environment is set up, run `pipenv shell` to enter it.

## Generating Your Database

Once you're in your environment, you can start development wherever you'd like.
We think it's easiest to start with setting up your database.

`cd` into the `lib/db` directory, then run `alembic init migrations` to set up
Alembic. Modify line 58 in `alembic.ini` to point to the database you intend to
create, then replace line 21 in `migrations/env.py` with the following:

```py
from models import Base
target_metadata = Base.metadata
```

We haven't created our `Base` or any models just yet, but we know where they're
going to be. Navigate to `models.py` and start creating those models. Remember
to regularly run `alembic revision --autogenerate -m'<descriptive message>'` and
`alembic upgrade head` to track your modifications to the database and create
checkpoints in case you ever need to roll those modifications back.

If you want to seed your database, now would be a great time to write out your
`seed.py` script and run it to generate some test data.

## Testing from project root
Run "python -m app.cli" in the terminal.

-You should now be able to run CLI commands.

## Running the commands

1. Create a new user
python -m app.cli create-user alice alice@example.com
Expected output:
User 'alice' created.

🔹 2. List all users
python -m app.cli list-users
Expected:
Users:
- ID: 3 | alice (alice@example.com)
- ID: 5 | Victor (Victor@example.com)

🔹 3. Generate and add a strong password (for account ID 3)
python -m app.cli generate-and-add-password 3
Expected:
Generated and added password for account ID 3:

🔹 4. Retrieve the password (account ID 3)
python -m app.cli get-password 3
Expected:

Decrypted password for account ID 3: mySecret123!

🔹 5. Delete the account (ID 3)

python -m app.cli delete-account 3

🔹 6. Delete the user (ID 3)

python -m app.cli delete-user 3


## To delete all users, accounts and passwords

Run "python lib/debug.py"

Expected:
All users, accounts, and passwords have been deleted.

-RE-seed the data after deleting to be able to now create new users.