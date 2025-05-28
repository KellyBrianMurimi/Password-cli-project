# models/password.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from lib.db import Base

class Password(Base):
    __tablename__ = 'passwords'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    encrypted_password = Column(String, nullable=False)

    account = relationship("Account", backref="passwords")
