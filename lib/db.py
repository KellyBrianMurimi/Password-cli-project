# lib/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///lib/securecli.db"

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()
