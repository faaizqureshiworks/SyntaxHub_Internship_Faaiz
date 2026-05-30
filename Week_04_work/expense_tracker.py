import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class ExpenseTracker:
    def __init__(self, filename="expenses.csv"):
        self.filename = filename
        self.headers = ["Date", "Type", "Category", "Amount"]
        self._initialize_file()

    def _initialize_file(self):
        """Creates the CSV file with headers if it doesn't exist."""
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)

    def add_entry(self, entry_type, category, amount):
        """Adds a new income or expense entry."""
        date_today = datetime.now().strftime("%Y-%m-%d")
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date_today, entry_type, category, amount])
        print(f"\n✅ Successfully added {entry_type}: {category} - Rs. {amount}")

    def view_summary(self):
        """Provides a summary of total income, expenses, and balance."""
        if not os.path.exists(self.filename) or os.stat(self.filename).st_size == 0:
            print("\n📂 No data found. Please add entries first.")
            return

        try:
            df = pd.read_csv(self.filename)
            if df.empty:
                print("\n📂 No data found in the file.")
                return

            total_income = df[df['Type'] == 'Income']['Amount'].sum()
            total_expense = df[df['Type'] == 'Expense']['Amount'].sum()
            balance = total_income - total_expense

            print("\n" + "="*30)
            print("💰 FINANCIAL SUMMARY")
            print("="*30)
            print(f"Total Income:  Rs. {total_income:.2f}")
            print(f"Total Expense: Rs. {total_expense:.2f}")
            print("-" * 30)
            print(f"Net Balance:   Rs. {balance:.2f}")
            print("="*30)
            
        except Exception as e:
            print(f"❌ Error reading data: {e}")

    def export_chart(self):
        """Generates and saves a pie chart of expenses."""
        try:
            df = pd.read_csv(self.filename)
            expenses = df[df['Type'] == 'Expense']
            
            if expenses.empty:
                print("\n❌ Not enough expense data to generate a chart.")
                return

            # Group by category and sum the amounts
            category_totals = expenses.groupby('Category')['Amount'].sum()

            # Create the Pie Chart
            plt.figure(figsize=(8, 6))
            plt.pie(category_totals, labels=category_totals.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
            plt.title('Expense Breakdown by Category')
            
            # Save the chart as an image
            chart_filename = "expense_chart.png"
            plt.savefig(chart_filename)
            print(f"\n📊 Success! Chart exported as '{chart_filename}' in your folder.")
            
        except Exception as e:
            print(f"❌ Error generating chart: {e}")


def main():
    tracker = ExpenseTracker()

    while True:
        print("\n--- 📈 Expense Tracker CLI ---")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Summary")
        print("4. Export Expense Chart")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            category = input("Enter Income Source (e.g., Salary, Freelance): ").strip().title()
            try:
                amount = float(input("Enter Amount: "))
                tracker.add_entry("Income", category, amount)
            except ValueError:
                print("❌ Invalid amount. Please enter a number.")

        elif choice == "2":
            category = input("Enter Expense Category (e.g., Food, Rent, Transport): ").strip().title()
            try:
                amount = float(input("Enter Amount: "))
                tracker.add_entry("Expense", category, amount)
            except ValueError:
                print("❌ Invalid amount. Please enter a number.")

        elif choice == "3":
            tracker.view_summary()

        elif choice == "4":
            tracker.export_chart()

        elif choice == "5":
            print("\n👋 Exiting Tracker. Have a great day!")
            break
        else:
            print("\n❌ Invalid choice! Please select 1-5.")

if __name__ == "__main__":
    main()