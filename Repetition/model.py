from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Numeric , CheckConstraint
from Database import Base


class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, index=True)
    holder_name = Column(String, nullable=False)
    balance = Column(Numeric(15, 2), nullable=False)
    transactions = relationship("Transaction", back_populates="account")

    __table_args__  = (
        CheckConstraint(
            "balance >= 0",
            name= "check_transaction_amount_positive"

        ),
    )


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False)
    transaction_type = Column(String, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    account = relationship("Account", back_populates="transactions")
