# Generate Customer, account number and Transaction ID

from datetime import datetime


def generate_customer_id(customers):
    return f"C{1001 + len(customers)}"


def generate_account_number(accounts):
    return f"A{100001 + len(accounts)}"


def generate_transaction_id(transactions):
    return f"T{100001 + len(transactions)}"


def today():
    return datetime.now().strftime("%Y-%m-%d")
