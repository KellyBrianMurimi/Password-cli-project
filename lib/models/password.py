from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Password(Base):
    __tablename__ = 'passwords'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    encrypted_password = Column(String, nullable=False)

    account = relationship("Account", back_populates="passwords")

    def __init__(self, account_id, encrypted_password):
        self.account_id = account_id
        self.encrypted_password = encrypted_password

    def __repr__(self):
        return f"<Password(id={self.id}, account_id={self.account_id})>"
