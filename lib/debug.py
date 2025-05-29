# lib/debug.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lib.db import Session
from lib.models.user import User
from lib.models.account import Account
from lib.models.password import Password

session = Session()

try:
    session.query(Password).delete()
    session.query(Account).delete()
    session.query(User).delete()
    session.commit()
    print(" All users, accounts, and passwords have been deleted.")
except Exception as e:
    session.rollback()
    print(" Error during deletion:", e)
finally:
    session.close()
