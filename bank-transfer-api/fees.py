from typing import Protocol

class FeeCalculator(Protocol):
    def calculate_fee(self, amount: int) -> float:
        ...

class Fees():
    @staticmethod
    def calculate_fee(feeamount: int) -> float:
        x = feeamount * 0.02
        return x

class PremiumFees():
    @staticmethod
    def calculate_fee(feeamount:int) -> float:
        x = feeamount * 0.01
        return x

class WrongFee:
    pass



