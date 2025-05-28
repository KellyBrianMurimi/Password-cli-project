# lib/models/password.py

from sqlalchemy import Column, Integer, String, ForeignKey
from lib.db import Base

class Password(Base):
    __tablename__ = 'passwords'

    id = Column(Integer, primary_key=True)
    encrypted_password = Column(String, nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'))
