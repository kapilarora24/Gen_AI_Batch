from dataclasses import dataclass, asdict


@dataclass
class Customer:
    customer_id: str
    name: str
    phone: str
    email: str
    
    def to_dict(self):
        return asdict(self)


@dataclass
class Account:
    account_number: str
    customer_id: str
    account_type: str
    balance: float

    def to_dict(self):
        return asdict(self)


@dataclass
class Transaction:
    transaction_id: str
    account_number: str
    transaction_type: str
    amount: float
    date: str
    remarks: str

    def to_dict(self):
        return asdict(self)
