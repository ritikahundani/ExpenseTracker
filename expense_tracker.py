import sqlite3
from datetime import datetime

# ----- DB Setup -----
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        amount REAL,
        description TEXT
    )
''')
conn.commit()

# ----- Functions -----
def add_expense():
    date = input("Enter date (YYYY-MM-DD) [default today]: ") or str(datetime.today().date())
    category = input("Enter category: ")
    amount = float(input("Enter amount: "))
    description = input("Enter description (optional): ")
    cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                   (date, category, amount, description))
    conn.commit()
    print("✅ Expense added!")

def view_expenses():
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()
    print("\n--- All Expenses ---")
    for row in rows:
        print(f"{row[0]} | {row[1]} | ₹{row[3]} | {row[2]} | {row[4]}")
    print("--------------------")

def total_by_category():
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    rows = cursor.fetchall()
    print("\n--- Total by Category ---")
    for row in rows:
        print(f"{row[0]}: ₹{row[1]}")
    print("--------------------------")

def delete_expense():
    view_expenses()
    try:
        exp_id = int(input("Enter ID of expense to delete: "))
        cursor.execute("DELETE FROM expenses WHERE id = ?", (exp_id,))
        conn.commit()
        print("🗑️ Expense deleted!")
    except:
        print("⚠️ Invalid ID!")

# ----- Menu -----
def menu():
    while True:
        print("\n📊 Expense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Total by Category")
        print("4. Delete Expense")
        print("5. Exit")

        choice = input("Choose option: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            total_by_category()
        elif choice == '4':
            delete_expense()
        elif choice == '5':
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid option!")

# ----- Run -----
if __name__ == "__main__":
    menu()
    conn.close()
