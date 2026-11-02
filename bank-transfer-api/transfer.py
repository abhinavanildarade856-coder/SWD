from fees import FeeCalculator

class Authentication:
    def __init__(self , name:str , fees:FeeCalculator) -> None:
        self.name  = name
        self.fees = fees
        
    def valid_amount(self , amount:int) -> int:
        if amount <= 0:
            raise ValueError("The value cannot smaller or equal to zero")
        return amount

    def show_user(self) -> None:
        print(self.name)

    def calculate_fee(self , amount:int) -> float:
        self.valid_amount(amount)
        return self.fees.calculate_fee(amount)

    
        

        
