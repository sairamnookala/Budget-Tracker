import json
from datetime import datetime

TRANSACTION_FILE = 'transactions.json'

class Transaction:
    def __init__(self, type, category, amount, date):
        self.type = type
        self.category = category
        self.amount = amount
        self.date = date

    def to_dict(self):
        return {
            'type': self.type,
            'category': self.category,
            'amount': self.amount,
            'date': self.date
        }

    @staticmethod
    def from_dict(data):
        return Transaction(data['type'], data['category'], data['amount'], data['date'])

def load_transactions():
    try:
        with open(TRANSACTION_FILE, 'r') as file:
            transactions_data = json.load(file)
            return [Transaction.from_dict(transaction) for transaction in transactions_data]
    except FileNotFoundError:
        return []

def save_transactions(transactions):
    with open(TRANSACTION_FILE, 'w') as file:
        json.dump([transaction.to_dict() for transaction in transactions], file, indent=4)

def add_transaction(type, category, amount):
    transactions = load_transactions()
    date = datetime.now().strftime("%Y-%m-%d")
    transactions.append(Transaction(type, category, amount, date))
    save_transactions(transactions)

def calculate_budget():
    transactions = load_transactions()
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')
    return total_income - total_expense

def analyze_expenses():
    transactions = load_transactions()
    expense_categories = {}
    for t in transactions:
        if t.type == 'expense':
            if t.category in expense_categories:
                expense_categories[t.category] += t.amount
            else:
                expense_categories[t.category] = t.amount
    return expense_categories

def list_transactions():
    transactions = load_transactions()
    for i, transaction in enumerate(transactions):
        print(f"{i + 1}. {transaction.type.capitalize()} | Category: {transaction.category} | Amount: ${transaction.amount} | Date: {transaction.date}")

def main():
    while True:
        print("\nBudget Tracker Application")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Calculate Budget")
        print("4. Analyze Expenses")
        print("5. List Transactions")
        print("6. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            category = input("Enter income category: ")
            amount = float(input("Enter income amount: "))
            add_transaction('income', category, amount)
        
        elif choice == '2':
            category = input("Enter expense category: ")
            amount = float(input("Enter expense amount: "))
            add_transaction('expense', category, amount)
        
        elif choice == '3':
            budget = calculate_budget()
            print(f"Remaining Budget: ${budget}")
        
        elif choice == '4':
            expenses = analyze_expenses()
            print("Expense Analysis:")
            for category, amount in expenses.items():
                print(f"Category: {category} | Total Spent: ${amount}")
        
        elif choice == '5':
            list_transactions()
        
        elif choice == '6':
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
