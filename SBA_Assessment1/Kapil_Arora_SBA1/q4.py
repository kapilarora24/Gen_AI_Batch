# Question 4: Safe Division
# Difficulty: Easy
# Topic: Python Exception Handling
#
# Problem Statement:
# Complete the exception handler so the function returns a friendly message
# when division by zero happens.
#
# Expected Output:
# Cannot divide by zero


def safe_divide(a, b):
    try:
        return round(a / b, 2)
    except ZeroDivisionError:
        return "Cannot divide by zero"


print(safe_divide(12, 0))
