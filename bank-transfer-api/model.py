from sqlalchemy import Column, Integer, String, Numeric
from databases import Base


class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer , primary_key=True , index=True)
    holder_name = Column(String , nullable=False)
    balance = Column(Numeric(15,2), nullable=False)




