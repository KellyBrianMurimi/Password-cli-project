from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Password(Base):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    encrypted_password = Column(String, nullable=False)

    # Relationship back to owning Account
    account = relationship("Account", back_populates="passwords")

    def __init__(self, *, encrypted_password: str, account):
        """Create a Password linked to an Account."""
        self.encrypted_password = encrypted_password
        self.account = account

    def __repr__(self):
        return f"<Password(id={self.id}, account_id={self.account_id})>"
