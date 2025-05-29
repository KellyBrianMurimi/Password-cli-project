from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    site = Column(String, nullable=False)
    username = Column(String, nullable=False)

    # Relationship back to the owning User
    user = relationship("User", back_populates="accounts")
    # One account can have many passwords; deleting account deletes passwords
    passwords = relationship("Password", back_populates="account", cascade="all, delete-orphan")

    def __init__(self, *, site: str, username: str, user):
        """Create an Account linked to a User."""
        self.site = site
        self.username = username
        self.user = user

    def __repr__(self):
        return f"<Account(id={self.id}, site='{self.site}', username='{self.username}', user_id={self.user_id})>"
