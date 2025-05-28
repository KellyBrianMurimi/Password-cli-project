# lib/models/password.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Password(Base):
    __tablename__ = 'passwords'

    id = Column(Integer, primary_key=True)
    encrypted_value = Column(String, nullable=False)

    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    account = relationship("Account", back_populates="passwords")
    user = relationship("User", back_populates="passwords")
