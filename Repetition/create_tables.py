from Database import engine , Base
from model import  Account
from model import Transaction

Base.metadata.create_all(bind=engine)

print("Connection Successfull !")