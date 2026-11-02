from fastapi import FastAPI , HTTPException , status , Depends
from pydantic import BaseModel , Field
from decimal import Decimal
from databases import sessionlocal
from model import Account
from sqlalchemy.orm import Session


app = FastAPI(title="Bank Transfer API")


def get_db():
    with  sessionlocal() as db:
        yield db    


class AccountCreate(BaseModel):
    holder_name: str
    initial_balance : Decimal = Field(ge=0)

class AccountResponse(BaseModel):
    account_id : int
    holder_name: str
    balance: Decimal


@app.get("/")
def home():
    return {"message":"Bank Transfer API"}






@app.post("/accounts" , 
          response_model=AccountResponse,
          status_code=status.HTTP_201_CREATED
          )

def create_accounts(account_data:AccountCreate ,db:Session = Depends(get_db)):
    new_account =  Account(
        holder_name = account_data.holder_name,
        balance= account_data.initial_balance
    )

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return {
        "account_id":new_account.account_id,
        "holder_name":new_account.holder_name,
        "balance": new_account.balance
    }






@app.get("/accounts/{account_id}", response_model=AccountResponse)

def get_account(account_id:int , db:Session = Depends(get_db)):
    account = db.query(Account).filter(
        Account.account_id == account_id
    ).first()


    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )

    return{
        "account_id":account.account_id,
        "holder_name":account.holder_name,
        "balance": account.balance
    }