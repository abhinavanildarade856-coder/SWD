from fastapi import HTTPException , FastAPI , status , Depends
from Database import sessionlocal
from model import  Account , Transaction
from sqlalchemy.orm import Session
from schema import AccountCreate , AccountRespond , TransactionCreate , AccountUpdate , TransactionRespond , AccountTransfer


app =  FastAPI(title="Bank API")

def get_db():
    with sessionlocal() as db:
        yield db


@app.get("/")
def home():
    return {"messgae":"Hello world my name is API"}



@app.post("/account",
          response_model=AccountRespond,
          status_code=status.HTTP_201_CREATED)
def Create_acc(account_data:AccountCreate , db:Session =  Depends(get_db)):
    new_account = Account(

        holder_name = account_data.holder_name,
        balance = account_data.initial_balance
    )

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return {
        "account_id": new_account.account_id,
        "holder_name": new_account.holder_name,
        "balance": new_account.balance
    }







@app.get("/accounts/{account_id}" , response_model=AccountRespond)
def get_account(account_id:int ,db:Session =  Depends(get_db)):
    account = db.query(Account).filter(
        Account.account_id == account_id
    ).first()

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account Not Found"
        )

    return {
        "account_id" : account.account_id,
        "holder_name": account.holder_name,
        "balance" : account.balance
    }



@app.patch("/accounts/{account_id}" , response_model=AccountRespond)
async def Update_name(account_id:int  ,update_name:AccountUpdate , db:Session = Depends(get_db)):
    account = db.query(Account).filter(
        Account.account_id == account_id
    ).first()

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No account exit"
        )

    account.holder_name = update_name.holder_name

    db.commit()
    db.refresh(account)

    return account






@app.post("/accounts/{account_id}/transactions" , status_code=status.HTTP_201_CREATED)
def create_transaction(account_id:int , transaction_data:TransactionCreate , db:Session = Depends(get_db)):
        account = db.query(Account).filter(
        Account.account_id == account_id).first()


        if account is None:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account Not Found"
        )


        if transaction_data.transaction_type == "withdrawal" and account.balance < transaction_data.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient balance for withdrawal"
            )
        try:
            if transaction_data.transaction_type == "deposit":
                account.balance += transaction_data.amount

            elif transaction_data.transaction_type == "withdrawal":
                account.balance -=   transaction_data.amount

            
            new_transaction = Transaction(
            account_id = account_id,
            transaction_type = transaction_data.transaction_type,
            amount = transaction_data.amount,
            )


            db.add(new_transaction)
            db.commit()
            db.refresh(new_transaction)

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail = "Trasaction failed due to an internal error"
            )

        return  new_transaction 




@app.get("/accounts/{account_id}/transactions",response_model=list[TransactionRespond])
def get_transactions(account_id:int , db:Session = Depends(get_db)):

    account = db.query(Account).filter(
        Account.account_id == account_id).first()

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account Not Found"
        )

    return account.transactions





@app.post("/transfer" , status_code=status.HTTP_201_CREATED)
def transfer(Transfer:AccountTransfer , db:Session = Depends(get_db)):

    if Transfer.to_account_id == Transfer.from_account_id:
        raise HTTPException(
            status_code=  status.HTTP_400_BAD_REQUEST,
            detail="You cannot tranfer money into youe own account"
        )

    to_acc = db.query(Account).filter(
        Account.account_id == Transfer.to_account_id
        ).first()

    if to_acc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not Found"
        )

    
    from_acc  = db.query(Account).filter(
        Account.account_id ==  Transfer.from_account_id
    ).first()

    if from_acc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )

    if Transfer.tranfer_amount > from_acc.balance or Transfer.tranfer_amount <= 0:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="There is Insufficient amount in the account"
        )



    try:
        from_acc.balance -= Transfer.tranfer_amount
        to_acc.balance += Transfer.tranfer_amount

        db.commit()
        db.refresh(to_acc)


    except Exception as e:
        db.rollback()
        raise

    return {
        "Message":"Transfer Sucessfull",
        "from_account_id": Transfer.from_account_id,
        "to_account_id": Transfer.to_account_id,
        "to_account_balance": to_acc.balance
    }

    

    

    





