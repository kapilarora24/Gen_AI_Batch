# generate autherization file

from storage import load_data
import os

print(os.getcwd())

USERS_FILE = "data/users.json"


def login():
    users = load_data(USERS_FILE)
    print(users)  # Debug
    """
    Validate username and password.
    Returns True if login is successful, otherwise False.
    """

    users = load_data(USERS_FILE)

    print("\n========== LOGIN ==========")

    username = input("Username : ")
    password = input("Password : ")

    for user in users:
        if user["username"] == username and user["password"] == password:
            print("\nLogin Successful.\n")
            return True

    print("\nInvalid Username or Password.\n")
    return False
