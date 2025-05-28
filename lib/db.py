# lib/db.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite DB path
DATABASE_URL = "sqlite:///lib/securecli.db"

# Create engine and session 
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)

# Base for ORM models
Base = declarative_base()
