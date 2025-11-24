import csv
import os
from datetime import datetime

EXPENSE_FILE = "expenses.csv"
BUDGET_FILE = "budget.txt"

def init_files():
    if not os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "date", "amount", "category", "description"])
    if not os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, "w") as f:
            f.write("0")

def read_budget():
    with open(BUDGET_FILE, "r") as f:
        return float(f.read().strip())

def write_budget(amount):
    with open(BUDGET_FILE, "w") as f:
        f.write(str(amount))

def get_next_id():
    max_id = 0
    if os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row and row[0].isdigit():
                    if int(row[0]) > max_id:
                        max_id = int(row[0])
    return str(max_id + 1)

def input_with_check(prompt):
    value = input(prompt)
    if value.strip() == "":
        print("Invalid input.")
        return None
    return value

def add_expense():
    amount_input = input_with_check("Enter amount: ₹")
    if amount_input is None:
        return
    try:
        amount = float(amount_input)
    except:
        print("Invalid amount.")
        return
    category = input_with_check("Enter category (Food/Travel/Shopping/Other): ")
    if category is None:
        return
    category = category.title()
    description = input("Short description (optional): ")
    date = datetime.now().strftime("%Y-%m-%d")
    expense_id = get_next_id()
    with open(EXPENSE_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([expense_id, date, amount, category, description])
    print("\nExpense added successfully!\n")

def view_expenses():
    print("\n------ ALL EXPENSES ------")
    total = 0
    with open(EXPENSE_FILE, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if not row or len(row) < 5:
                continue
            eid, date, amount, category, desc = row
            print(f"ID:{eid} | {date} | ₹{amount} | {category} | {desc}")
            try:
                total += float(amount)
            except:
                continue
    print(f"\nTotal Spending: ₹{total}\n")

def monthly_summary():
    print("\n------ MONTHLY SUMMARY ------")
    current_month = datetime.now().strftime("%Y-%m")
    summary = {}
    total = 0
    with open(EXPENSE_FILE, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if not row or len(row) < 5:
                continue
            eid, date, amount, category, desc = row
            if date.startswith(current_month):
                try:
                    amount = float(amount)
                except:
                    continue
                total += amount
                if category in summary:
                    summary[category] += amount
                else:
                    summary[category] = amount
    print("\nCategory-wise spending this month:")
    for cat, amt in summary.items():
        print(f" - {cat}: ₹{amt}")
    print(f"\nTotal this month: ₹{total}")
    budget = read_budget()
    if budget > 0:
        print(f"Monthly Budget: ₹{budget}")
        if total > budget:
            print("ALERT: You exceeded your monthly budget!")
    print()

def set_budget():
    amount_input = input_with_check("Enter new monthly budget (₹): ")
    if amount_input is None:
        return
    try:
        amount = float(amount_input)
    except:
        print("Invalid amount.")
        return
    write_budget(amount)
    print("\nMonthly budget updated!\n")

def delete_expense():
    print("\n------ DELETE EXPENSE ------")
    expense_id = input_with_check("Enter ID of expense to delete: ")
    if expense_id is None:
        return
    rows = []
    deleted = False
    with open(EXPENSE_FILE, "r") as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if row and row[0] == expense_id:
                deleted = True
                continue
            rows.append(row)
    with open(EXPENSE_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)
    if deleted:
        print("\nExpense deleted successfully!\n")
    else:
        print("\nExpense not found.\n")

def main():
    init_files()
    while True:
        print("====== DAILY EXPENSE TRACKER ======")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Monthly Summary")
        print("4. Set Monthly Budget")
        print("5. Delete Expense")
        print("6. Exit")
        choice = input_with_check("\nEnter your choice: ")
        if choice is None:
            continue
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            monthly_summary()
        elif choice == "4":
            set_budget()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            print("THANKS FOR USING OUR SOFTWARE")
            break
        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()
