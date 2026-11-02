from databases import engine , Base
from model import Account

Base.metadata.create_all(bind=engine)

print("Tables created Sucessfully !")

