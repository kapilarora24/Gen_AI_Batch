from auth import login
from bank import (
    create_customer,
    create_account,
    deposit,
    withdraw,
    transfer,
    account_statement,
    search_transactions,
)


def show_menu():
    print("\n" + "=" * 50)
    print("  MINI BANKING MANAGEMENT SYSTEM")
    print("=" * 50)
    print("1. Create Customer")
    print("2. Create Account")
    print("3. Deposit Money")
    print("4. Withdraw Money")
    print("5. Transfer Money")
    print("6. Account Statement")
    print("7. Search Transactions")
    print("8. Logout")
    print("9. Exit")
    print("=" * 50)


def main():

    print("=" * 50)
    print(" Welcome to Mini Banking Management System ")
    print("=" * 50)

    # Login until success
    while True:
        if login():
            break
        print("Please try again.\n")

    while True:

        show_menu()

        choice = input("Enter your choice : ")

        if choice == "1":
            create_customer()

        elif choice == "2":
            create_account()

        elif choice == "3":
            deposit()

        elif choice == "4":
            withdraw()

        elif choice == "5":
            transfer()

        elif choice == "6":
            account_statement()

        elif choice == "7":
            search_transactions()

        elif choice == "8":
            print("\nLogging out...\n")

            while True:
                if login():
                    break

        elif choice == "9":
            print("\nThank you for using Mini Banking System.")
            break

        else:
            print("\nInvalid Choice. Please try again.")


if __name__ == "__main__":
    main()
