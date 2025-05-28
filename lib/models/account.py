from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    account_name = Column(String, nullable=False)
    account_type = Column(String, nullable=False)

    user = relationship("User", back_populates="accounts")
    passwords = relationship("Password", back_populates="account", cascade="all, delete-orphan")

    def __init__(self, user_id, account_name, account_type):
        self.user_id = user_id
        self.account_name = account_name
        self.account_type = account_type

    def __repr__(self):
        return f"<Account(id={self.id}, account_name='{self.account_name}', account_type='{self.account_type}', user_id={self.user_id})>"
