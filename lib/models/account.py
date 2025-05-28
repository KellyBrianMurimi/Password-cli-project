# lib/models/account.py

from sqlalchemy import Column, Integer, String, ForeignKey
from lib.db import Base

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

