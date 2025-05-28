# lib/models/user.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)

    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")
    passwords = relationship("Password", back_populates="user", cascade="all, delete-orphan")
