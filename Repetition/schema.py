from pydantic import BaseModel , Field , ValidationError, validator
from decimal import Decimal
from typing import Optional , Literal
from datetime import datetime


class AccountCreate(BaseModel):
    holder_name: str
    initial_balance:Decimal = Field(ge=0)

class AccountRespond(BaseModel):
    account_id : int
    holder_name:str
    balance: Decimal

class TransactionCreate(BaseModel):
    transaction_type: Literal["deposit" , "withdrawal"] 
    amount:Decimal = Field(ge=0)

class AccountUpdate(BaseModel):
    holder_name:str

class TransactionRespond(BaseModel):
    transaction_id:int
    account_id:int
    transaction_type: str
    amount:Decimal
    created_at: datetime

    model_config = {"from_attributes":True}

class AccountTransfer(BaseModel):
    from_account_id: int
    to_account_id : int
    tranfer_amount : Decimal = Field(gt=0)