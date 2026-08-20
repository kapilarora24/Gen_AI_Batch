from models import Customer, Account, Transaction
from storage import load_data, save_data
from utils import (
    generate_customer_id,
    generate_account_number,
    generate_transaction_id,
    today,
)

CUSTOMERS_FILE = "data/customers.json"
ACCOUNTS_FILE = "data/accounts.json"
TRANSACTIONS_FILE = "data/transactions.json"


# Cretae Customer
def create_customer():
    customers = load_data(CUSTOMERS_FILE)

    print("\n===== Create Customer =====")

    name = input("Name    : ")
    phone = input("Phone   : ")
    email = input("Email   : ")

    customer = Customer(
        customer_id=generate_customer_id(customers),
        name=name,
        phone=phone,
        email=email,
    )

    customers.append(customer.to_dict())

    save_data(CUSTOMERS_FILE, customers)

    print("\nCustomer Created Successfully")
    print("Customer ID :", customer.customer_id)


# create Account
def create_account():
    customers = load_data(CUSTOMERS_FILE)
    accounts = load_data(ACCOUNTS_FILE)

    print("\n===== Create Account =====")

    customer_id = input("Customer ID : ")

    customer = next(
        (c for c in customers if c["customer_id"] == customer_id),
        None,
    )

    if customer is None:
        print("Customer not found.")
        return

    account_type = input("Account Type (Savings/Current): ")

    try:
        opening_balance = float(input("Opening Balance : "))
    except ValueError:
        print("Invalid amount.")
        return

    account = Account(
        account_number=generate_account_number(accounts),
        customer_id=customer_id,
        account_type=account_type,
        balance=opening_balance,
    )

    accounts.append(account.to_dict())

    save_data(ACCOUNTS_FILE, accounts)

    print("\nAccount Created Successfully")
    print("Account Number :", account.account_number)


# Deposit Money
def deposit():
    accounts = load_data(ACCOUNTS_FILE)
    transactions = load_data(TRANSACTIONS_FILE)

    print("\n===== Deposit Money =====")

    account_number = input("Account Number : ")

    account = next(
        (a for a in accounts if a["account_number"] == account_number),
        None,
    )

    if account is None:
        print("Account not found.")
        return

    try:
        amount = float(input("Deposit Amount : "))
    except ValueError:
        print("Invalid amount.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    account["balance"] += amount

    transaction = Transaction(
        transaction_id=generate_transaction_id(transactions),
        account_number=account_number,
        transaction_type="Deposit",
        amount=amount,
        date=today(),
        remarks="Cash Deposit",
    )

    transactions.append(transaction.to_dict())

    save_data(ACCOUNTS_FILE, accounts)
    save_data(TRANSACTIONS_FILE, transactions)

    print("\nDeposit Successful")
    print("Current Balance :", account["balance"])


# Withdraw Money
def withdraw():
    accounts = load_data(ACCOUNTS_FILE)
    transactions = load_data(TRANSACTIONS_FILE)

    print("\n===== Withdraw Money =====")

    account_number = input("Account Number : ")

    account = next(
        (a for a in accounts if a["account_number"] == account_number),
        None,
    )

    if account is None:
        print("Account not found.")
        return

    try:
        amount = float(input("Withdraw Amount : "))
    except ValueError:
        print("Invalid amount.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    if amount > account["balance"]:
        print("Insufficient Balance")
        return

    account["balance"] -= amount

    transaction = Transaction(
        transaction_id=generate_transaction_id(transactions),
        account_number=account_number,
        transaction_type="Withdraw",
        amount=amount,
        date=today(),
        remarks="Cash Withdrawal",
    )

    transactions.append(transaction.to_dict())

    save_data(ACCOUNTS_FILE, accounts)
    save_data(TRANSACTIONS_FILE, transactions)

    print("\nWithdrawal Successful")
    print("Current Balance :", account["balance"])


# Transfer money
def transfer():
    accounts = load_data(ACCOUNTS_FILE)
    transactions = load_data(TRANSACTIONS_FILE)

    print("\n===== Transfer Money =====")

    from_account = input("From Account : ")
    to_account = input("To Account   : ")

    if from_account == to_account:
        print("Cannot transfer to the same account.")
        return

    sender = next(
        (a for a in accounts if a["account_number"] == from_account),
        None,
    )

    receiver = next(
        (a for a in accounts if a["account_number"] == to_account),
        None,
    )

    if sender is None or receiver is None:
        print("One or both accounts do not exist.")
        return

    try:
        amount = float(input("Amount : "))
    except ValueError:
        print("Invalid amount.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    if sender["balance"] < amount:
        print("Insufficient Balance")
        return

    sender["balance"] -= amount
    receiver["balance"] += amount

    transactions.append(
        Transaction(
            generate_transaction_id(transactions),
            from_account,
            "Transfer",
            amount,
            today(),
            f"Transferred to {to_account}",
        ).to_dict()
    )

    transactions.append(
        Transaction(
            generate_transaction_id(transactions),
            to_account,
            "Deposit",
            amount,
            today(),
            f"Received from {from_account}",
        ).to_dict()
    )

    save_data(ACCOUNTS_FILE, accounts)
    save_data(TRANSACTIONS_FILE, transactions)

    print("\nTransfer Successful")


# Account Statments
def account_statement():
    accounts = load_data(ACCOUNTS_FILE)
    transactions = load_data(TRANSACTIONS_FILE)

    account_number = input("Account Number : ")

    account = next(
        (a for a in accounts if a["account_number"] == account_number),
        None,
    )

    if account is None:
        print("Account not found.")
        return

    print("\n========== ACCOUNT STATEMENT ==========")
    print("Account Number :", account["account_number"])
    print("Balance        :", account["balance"])

    print("\nTransactions")
    print("-" * 50)

    found = False

    for transaction in transactions:
        if transaction["account_number"] == account_number:
            found = True
            print(
                transaction["date"],
                "|",
                transaction["transaction_type"],
                "|",
                transaction["amount"],
                "|",
                transaction["remarks"],
            )

    if not found:
        print("No transactions found.")


# Search Transactiopn
def search_transactions():
    transactions = load_data(TRANSACTIONS_FILE)

    print("\nSearch By")
    print("1. Date")
    print("2. Type")
    print("3. Amount")

    choice = input("Choice : ")

    if choice == "1":
        value = input("Enter Date (YYYY-MM-DD): ")

        results = [t for t in transactions if t["date"] == value]

    elif choice == "2":
        value = input("Transaction Type : ").capitalize()

        results = [t for t in transactions if t["transaction_type"] == value]

    elif choice == "3":
        try:
            value = float(input("Amount : "))
        except ValueError:
            print("Invalid amount.")
            return

        results = [t for t in transactions if t["amount"] == value]

    else:
        print("Invalid Choice")
        return

    print("\nSearch Result")
    print("-" * 60)

    if not results:
        print("No matching transactions found.")
        return

    for transaction in results:
        print(transaction)
