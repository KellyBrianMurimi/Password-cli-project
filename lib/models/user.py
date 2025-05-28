from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)

    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
