import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# Get the database URL from environment or default to a local SQLite file
db_path = os.getenv("DATABASE_URL", "sqlite:///securecli.db")

# Normalize the path if using SQLite (convert relative to absolute path)
if db_path.startswith("sqlite:///"):
    local_path = db_path.replace("sqlite:///", "")
    abs_path = Path(local_path).resolve()
    DATABASE_URL = f"sqlite:///{abs_path}"
else:
    DATABASE_URL = db_path

print("Using database:", DATABASE_URL)

# Create the engine and session factory
engine = create_engine(DATABASE_URL, echo=False, future=True)
Session = sessionmaker(bind=engine, future=True)

# Base class for declarative models
Base = declarative_base()
