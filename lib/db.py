import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# Getting the database URL 
db_path = os.getenv("DATABASE_URL", "sqlite:///securecli.db")

# Normalizing the path 
if db_path.startswith("sqlite:///"):
    local_path = db_path.replace("sqlite:///", "")
    abs_path = Path(local_path).resolve()
    DATABASE_URL = f"sqlite:///{abs_path}"
else:
    DATABASE_URL = db_path

print("Using database:", DATABASE_URL)

# Engine and session factory
engine = create_engine(DATABASE_URL, echo=False, future=True)
Session = sessionmaker(bind=engine, future=True)

# Base class for declarative models
Base = declarative_base()
