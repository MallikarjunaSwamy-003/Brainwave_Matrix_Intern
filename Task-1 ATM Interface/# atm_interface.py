# atm_interface.py

import getpass
import sys

class ATM:
    def __init__(self, user_pin, balance=0):
        self.correct_pin = user_pin
        self.balance = balance
        self.history = []

    def authenticate(self):
        print("===== Welcome to Python ATM =====")
        for _ in range(3):
            pin = getpass.getpass("Enter your 4-digit PIN: ")
            if pin == self.correct_pin:
                print("Authentication successful.\n")
                return True
            else:
                print("Incorrect PIN. Try again.")
        print("Too many incorrect attempts. Exiting.")
        return False

    def display_menu(self):
        print("""
========= ATM Menu =========
1. Check Balance
2. Deposit Money
3. Withdraw Money
4. View Transaction History
5. Exit
""")

    def check_balance(self):
        print(f"Current Balance: ₹{self.balance}")

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.history.append(f"Deposited ₹{amount}")
            print(f"₹{amount} deposited successfully.")
        else:
            print("Invalid amount.")

    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid amount.")
        elif amount > self.balance:
            print("Insufficient balance.")
        else:
            self.balance -= amount
            self.history.append(f"Withdrew ₹{amount}")
            print(f"₹{amount} withdrawn successfully.")

    def show_history(self):
        if not self.history:
            print("No transactions yet.")
        else:
            print("Transaction History:")
            for txn in self.history:
                print(" -", txn)

    def run(self):
        if not self.authenticate():
            sys.exit()

        while True:
            self.display_menu()
            choice = input("Choose an option: ")

            if choice == '1':
                self.check_balance()
            elif choice == '2':
                try:
                    amount = float(input("Enter amount to deposit: ₹"))
                    self.deposit(amount)
                except ValueError:
                    print("Enter a valid number.")
            elif choice == '3':
                try:
                    amount = float(input("Enter amount to withdraw: ₹"))
                    self.withdraw(amount)
                except ValueError:
                    print("Enter a valid number.")
            elif choice == '4':
                self.show_history()
            elif choice == '5':
                print("Thank you for using Python ATM. Goodbye!")
                break
            else:
                print("Invalid option. Try again.")

# ---- Run ATM ----
if __name__ == "__main__":
    my_atm = ATM(user_pin="1234", balance=5000)  # Default PIN: 1234
    my_atm.run()