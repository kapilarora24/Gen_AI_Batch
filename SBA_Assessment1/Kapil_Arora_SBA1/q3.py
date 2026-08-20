# Question 3: Update Account Balance
# Difficulty: Easy
# Topic: Python OOP
#
# Problem Statement:
# Complete the `deposit` method so it adds the deposit amount to the current balance.
#
# Expected Output:
# 750


class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount


account = BankAccount("Riya", 500)
account.deposit(250)
print(account.balance)
