import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from datetime import datetime
from tkinter import simpledialog
import tkinter.simpledialog as simpledialog

# PostgreSQL database connection
conn = psycopg2.connect(
    dbname="dbms_project",
    user="postgres",
    password="pgadmin4",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

class PersonalFinanceTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("800x500")
        self.style = ttk.Style()
        self.style.configure('TButton', padding=5, relief="flat")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        self.expense_frame = ttk.Frame(self.notebook)
        self.income_frame = ttk.Frame(self.notebook)
        self.budget_frame = ttk.Frame(self.notebook)
        self.report_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.expense_frame, text='Expenses')
        self.notebook.add(self.income_frame, text='Income')
        self.notebook.add(self.budget_frame, text='Budget')
        self.notebook.add(self.report_frame, text='Report')

        self.create_expense_widgets()
        self.create_income_widgets()
        self.create_budget_widgets()
        self.create_report_widgets()

    def create_expense_widgets(self):
        # Label for Expense
        ttk.Label(self.expense_frame, text="Expenses", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Treeview for Expense
        self.expense_tree = ttk.Treeview(self.expense_frame, columns=('S.no', 'Date', 'Amount', 'Category', 'Notes'), show='headings')
        self.expense_tree.heading('S.no', text='S.no')
        self.expense_tree.heading('Date', text='Date')
        self.expense_tree.heading('Amount', text='Amount')
        self.expense_tree.heading('Category', text='Category')
        self.expense_tree.heading('Notes', text='Notes')
        self.expense_tree.pack(padx=20, pady=10)

        # Scrollbar for Expense Treeview
        expense_scroll = ttk.Scrollbar(self.expense_frame, orient="vertical", command=self.expense_tree.yview)
        expense_scroll.pack(side='right', fill='y')
        self.expense_tree.config(yscrollcommand=expense_scroll.set)

        # Buttons for Expense
        expense_buttons_frame = ttk.Frame(self.expense_frame)
        expense_buttons_frame.pack(pady=10)

        ttk.Button(expense_buttons_frame, text="Add Expense", command=self.add_expense).pack(side='left', padx=5)
        ttk.Button(expense_buttons_frame, text="Edit Expense", command=self.edit_expense).pack(side='left', padx=5)
        ttk.Button(expense_buttons_frame, text="Delete Expense", command=self.delete_expense).pack(side='left', padx=5)

        # Load Expenses
        self.load_expenses()

    def create_income_widgets(self):
        # Label for Income
        ttk.Label(self.income_frame, text="Income", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Treeview for Income
        self.income_tree = ttk.Treeview(self.income_frame, columns=('S.no', 'Date', 'Amount', 'Source'), show='headings')
        self.income_tree.heading('S.no', text='S.no')
        self.income_tree.heading('Date', text='Date')
        self.income_tree.heading('Amount', text='Amount')
        self.income_tree.heading('Source', text='Source')
        self.income_tree.pack(padx=20, pady=10)

        # Scrollbar for Income Treeview
        income_scroll = ttk.Scrollbar(self.income_frame, orient="vertical", command=self.income_tree.yview)
        income_scroll.pack(side='right', fill='y')
        self.income_tree.config(yscrollcommand=income_scroll.set)

        # Buttons for Income
        income_buttons_frame = ttk.Frame(self.income_frame)
        income_buttons_frame.pack(pady=10)

        ttk.Button(income_buttons_frame, text="Add Income", command=self.add_income).pack(side='left', padx=5)
        ttk.Button(income_buttons_frame, text="Edit Income", command=self.edit_income).pack(side='left', padx=5)
        ttk.Button(income_buttons_frame, text="Delete Income", command=self.delete_income).pack(side='left', padx=5)

        # Load Income
        self.load_income()

    def create_budget_widgets(self):
        # Label for Budget
        ttk.Label(self.budget_frame, text="Budget", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Treeview for Budget
        self.budget_tree = ttk.Treeview(self.budget_frame, columns=('S.no', 'Category', 'Budget Limit', 'Spent'), show='headings')
        self.budget_tree.heading('S.no', text='S.no')
        self.budget_tree.heading('Category', text='Category')
        self.budget_tree.heading('Budget Limit', text='Budget Limit')
        self.budget_tree.heading('Spent', text='Spent')
        self.budget_tree.pack(padx=20, pady=10)

        # Scrollbar for Budget Treeview
        budget_scroll = ttk.Scrollbar(self.budget_frame, orient="vertical", command=self.budget_tree.yview)
        budget_scroll.pack(side='right', fill='y')
        self.budget_tree.config(yscrollcommand=budget_scroll.set)

        # Buttons for Budget
        budget_buttons_frame = ttk.Frame(self.budget_frame)
        budget_buttons_frame.pack(pady=10)

        ttk.Button(budget_buttons_frame, text="Add Budget", command=self.add_budget).pack(side='left', padx=5)
        ttk.Button(budget_buttons_frame, text="Edit Budget", command=self.edit_budget).pack(side='left', padx=5)
        ttk.Button(budget_buttons_frame, text="Delete Budget", command=self.delete_budget).pack(side='left', padx=5)

        # Load Budgets
        self.load_budgets()


    def create_report_widgets(self):
        # Label for Report
        ttk.Label(self.report_frame, text="Financial Report", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        # Text widget for Report
        self.report_text = tk.Text(self.report_frame, height=20, width=50)
        self.report_text.pack(padx=20, pady=10)
        
        # Frame for buttons
        report_button_frame = ttk.Frame(self.report_frame)
        report_button_frame.pack(pady=10)
        
        # Button for generating Report
        ttk.Button(report_button_frame, text="Generate Report", command=self.generate_report).pack(side='left', padx=5)
        
        # Button for exporting Report
        ttk.Button(report_button_frame, text="Export Report", command=self.export_report).pack(side='left', padx=5)

    def load_expenses(self):
        # Function to load expenses data into expense treeview
        self.expense_tree.delete(*self.expense_tree.get_children())
        cur.execute("SELECT * FROM expenses")
        expenses = cur.fetchall()
        for expense in expenses:
            self.expense_tree.insert('', 'end', values=expense)

    def add_expense(self):
    # Function to add a new expense
        def save_new_expense():
            date = expense_date_entry.get()
            amount = float(expense_amount_entry.get())
            category = expense_category_entry.get()
            notes = expense_notes_entry.get()

            # Insert values into the Treeview columns at the correct index
            self.expense_tree.insert('', 'end', values=(date, amount, category, notes))

            # Insert values into the database
            cur.execute("INSERT INTO expenses (date, amount, category, notes) VALUES (%s, %s, %s, %s)", (date, amount, category, notes))
            conn.commit()

            expense_dialog.destroy()
            self.load_expenses()

        expense_dialog = tk.Toplevel(self.root)
        expense_dialog.title("Add New Expense")

        ttk.Label(expense_dialog, text="Date:").grid(row=0, column=0, padx=5, pady=5)
        expense_date_entry = ttk.Entry(expense_dialog)
        expense_date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(expense_dialog, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        expense_amount_entry = ttk.Entry(expense_dialog)
        expense_amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(expense_dialog, text="Category:").grid(row=2, column=0, padx=5, pady=5)
        expense_category_entry = ttk.Entry(expense_dialog)
        expense_category_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(expense_dialog, text="Notes:").grid(row=3, column=0, padx=5, pady=5)
        expense_notes_entry = ttk.Entry(expense_dialog)
        expense_notes_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(expense_dialog, text="Save", command=save_new_expense).grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def edit_expense(self):
        selected_item = self.expense_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select an expense to edit.")
            return

        item_values = self.expense_tree.item(selected_item, 'values')
        if not item_values:
            messagebox.showerror("Error", "Selected expense does not have complete details.")
            return

        item_id = item_values[0]
        initial_date, initial_amount, initial_category, initial_notes = item_values[1:]

        # Create a dialog to edit the expense
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Expense")

        # Labels and entry widgets for editing
        ttk.Label(dialog, text="Date:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        date_entry = ttk.Entry(dialog)
        date_entry.grid(row=0, column=1, padx=5, pady=5)
        date_entry.insert(0, initial_date)  # Insert initial date value

        ttk.Label(dialog, text="Amount:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        amount_entry = ttk.Entry(dialog)
        amount_entry.grid(row=1, column=1, padx=5, pady=5)
        amount_entry.insert(0, initial_amount)  # Insert initial amount value

        ttk.Label(dialog, text="Category:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        category_entry = ttk.Entry(dialog)
        category_entry.grid(row=2, column=1, padx=5, pady=5)
        category_entry.insert(0, initial_category)  # Insert initial category value

        ttk.Label(dialog, text="Notes:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        notes_entry = ttk.Entry(dialog)
        notes_entry.grid(row=3, column=1, padx=5, pady=5)
        notes_entry.insert(0, initial_notes)  # Insert initial notes value

        # Function to save the edited expense
        def save_edited_expense():
            new_date = date_entry.get()
            new_amount = amount_entry.get()
            new_category = category_entry.get()
            new_notes = notes_entry.get()

            # Update the database with edited expense details
            query = "UPDATE expenses SET date = %s, amount = %s, category = %s, notes = %s WHERE id = %s"
            cur.execute(query, (new_date, new_amount, new_category, new_notes, item_id))
            conn.commit()

            # Reload expenses after editing
            self.load_expenses()
            dialog.destroy()

        # Button to save the edited expense
        ttk.Button(dialog, text="Save", command=save_edited_expense).grid(row=4, columnspan=2, padx=5, pady=10)

    def delete_expense(self):
        selected_item = self.expense_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an expense to delete.")
            return

        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete the selected expense?")
        if confirm:
            item_id = self.expense_tree.item(selected_item, 'values')[0]
            if not item_id:
                messagebox.showerror("Error", "Unexpected data format for the selected expense.")
                return

            # Delete expense from the database
            cur.execute("DELETE FROM expenses WHERE id = %s", (item_id,))
            conn.commit()

            # Delete expense from the Treeview
            self.expense_tree.delete(selected_item)
            
    def load_income(self):
            # Function to load income data into income treeview
            self.income_tree.delete(*self.income_tree.get_children())
            cur.execute("SELECT * FROM income")
            income = cur.fetchall()
            for item in income:
                self.income_tree.insert('', 'end', values=item)

    def add_income(self):
        # Function to add a new income entry
        def save_new_income():
            date = income_date_entry.get()
            amount = float(income_amount_entry.get())
            source = income_source_entry.get()

            # Insert values into the Treeview columns at the correct index
            self.income_tree.insert('', 'end', values=(date, amount, source))

            # Insert values into the database
            cur.execute("INSERT INTO income (date, amount, source) VALUES (%s, %s, %s)", (date, amount, source))
            conn.commit()

            income_dialog.destroy()
            self.load_income()

        income_dialog = tk.Toplevel(self.root)
        income_dialog.title("Add New Income")

        ttk.Label(income_dialog, text="Date:").grid(row=0, column=0, padx=5, pady=5)
        income_date_entry = ttk.Entry(income_dialog)
        income_date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(income_dialog, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        income_amount_entry = ttk.Entry(income_dialog)
        income_amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(income_dialog, text="Source:").grid(row=2, column=0, padx=5, pady=5)
        income_source_entry = ttk.Entry(income_dialog)
        income_source_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(income_dialog, text="Save", command=save_new_income).grid(row=3, column=0, columnspan=2, padx=5, pady=5)


    def save_income(self):
        # Function to save new income entry
        def save_new_income():
            date = income_date_entry.get()
            amount = float(income_amount_entry.get())
            source = income_source_entry.get()

            # Insert values into the Treeview columns at the correct index
            self.income_tree.insert('', 'end', values=(date, amount, source))

            # Insert values into the database
            cur.execute("INSERT INTO income (date, amount, source) VALUES (%s, %s, %s)", (date, amount, source))
            conn.commit()

            income_dialog.destroy()
            self.load_income()

        income_dialog = tk.Toplevel(self.root)
        income_dialog.title("Add New Income")

        ttk.Label(income_dialog, text="Date:").grid(row=0, column=0, padx=5, pady=5)
        income_date_entry = ttk.Entry(income_dialog)
        income_date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(income_dialog, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        income_amount_entry = ttk.Entry(income_dialog)
        income_amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(income_dialog, text="Source:").grid(row=2, column=0, padx=5, pady=5)
        income_source_entry = ttk.Entry(income_dialog)
        income_source_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(income_dialog, text="Save", command=save_new_income).grid(row=3, column=0, columnspan=2, padx=5, pady=5)


    def edit_income(self):
        selected_item = self.income_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select an income entry to edit.")
            return

        item_values = self.income_tree.item(selected_item, 'values')
        if not item_values:
            messagebox.showerror("Error", "Selected income entry does not have complete details.")
            return

        item_id = item_values[0]
        initial_date, initial_amount, initial_source = item_values[1:]

        # Create a dialog to edit the income entry
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Income Entry")

        # Labels and entry widgets for editing
        ttk.Label(dialog, text="Date:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        date_entry = ttk.Entry(dialog)
        date_entry.grid(row=0, column=1, padx=5, pady=5)
        date_entry.insert(0, initial_date)  # Insert initial date value

        ttk.Label(dialog, text="Amount:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        amount_entry = ttk.Entry(dialog)
        amount_entry.grid(row=1, column=1, padx=5, pady=5)
        amount_entry.insert(0, initial_amount)  # Insert initial amount value

        ttk.Label(dialog, text="Source:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        source_entry = ttk.Entry(dialog)
        source_entry.grid(row=2, column=1, padx=5, pady=5)
        source_entry.insert(0, initial_source)  # Insert initial source value

        # Function to save the edited income entry
        def save_edited_income():
            new_date = date_entry.get()
            new_amount = amount_entry.get()
            new_source = source_entry.get()

            # Update the database with edited income entry details
            query = "UPDATE income SET date = %s, amount = %s, source = %s WHERE id = %s"
            cur.execute(query, (new_date, new_amount, new_source, item_id))
            conn.commit()

            # Reload income entries after editing
            self.load_income()
            dialog.destroy()

        # Button to save the edited income entry
        ttk.Button(dialog, text="Save", command=save_edited_income).grid(row=3, columnspan=2, padx=5, pady=10)


    def delete_income(self):
        selected_item = self.income_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an income entry to delete.")
            return

        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete the selected income entry?")
        if confirm:
            item_id = self.income_tree.item(selected_item, 'values')[0]
            if not item_id:
                messagebox.showerror("Error", "Unexpected data format for the selected income entry.")
                return

            # Delete the income entry from the database
            cur.execute("DELETE FROM income WHERE id = %s", (item_id,))
            conn.commit()

            # Delete the income entry from the treeview
            self.income_tree.delete(selected_item)


    def load_budgets(self):
        # Function to load budget data into budget treeview
        self.budget_tree.delete(*self.budget_tree.get_children())
        cur.execute("SELECT * FROM budgets")
        budgets = cur.fetchall()
        for budget in budgets:
            self.budget_tree.insert('', 'end', values=budget)

    def add_budget(self):
        # Function to add a new budget entry
        def save_new_budget():
            category = str(budget_category_entry.get())  # Ensure that category is treated as a string
            budget_limit = float(budget_limit_entry.get())
            spent = float(budget_spent_entry.get())

            # Insert values into the treeview columns at the correct index
            self.budget_tree.insert('', 'end', values=(category, budget_limit, spent))

            # Insert values into the database
            cur.execute("INSERT INTO budgets (category, budget_limit, spent) VALUES (%s, %s, %s)", (category, budget_limit, spent))
            conn.commit()

            budget_dialog.destroy()
            self.load_budgets()

        budget_dialog = tk.Toplevel(self.root)
        budget_dialog.title("Add New Budget")

        ttk.Label(budget_dialog, text="Category:").grid(row=0, column=0, padx=5, pady=5)
        budget_category_entry = ttk.Entry(budget_dialog)
        budget_category_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(budget_dialog, text="Budget Limit:").grid(row=1, column=0, padx=5, pady=5)
        budget_limit_entry = ttk.Entry(budget_dialog)
        budget_limit_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(budget_dialog, text="Spent:").grid(row=2, column=0, padx=5, pady=5)
        budget_spent_entry = ttk.Entry(budget_dialog)
        budget_spent_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(budget_dialog, text="Save", command=save_new_budget).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def delete_budget(self):
        # Function to delete a budget entry
        selected_item = self.budget_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a budget entry to delete.")
            return

        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete the selected budget entry?")
        if confirm:
            item_id = self.budget_tree.item(selected_item, 'values')[0]
            if not item_id:
                messagebox.showerror("Error", "Unexpected data format for the selected budget entry.")
                return

            # Delete budget entry from the database
            cur.execute("DELETE FROM budgets WHERE id = %s", (item_id,))
            conn.commit()

            # Delete budget entry from the Treeview
            self.budget_tree.delete(selected_item)


    def edit_budget(self):
        # Function to edit an existing budget entry
        selected_item = self.budget_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a budget entry to edit.")
            return

        item_id = self.budget_tree.item(selected_item, 'values')[0]
        if not item_id:
            messagebox.showerror("Error", "Selected budget entry does not have complete details.")
            return

        # Create a dialog to edit the budget entry
        budget_dialog = tk.Toplevel(self.root)
        budget_dialog.title("Edit Budget")

        # Labels and entry widgets for editing
        ttk.Label(budget_dialog, text="Category:").grid(row=0, column=0, padx=5, pady=5)
        category_entry = ttk.Entry(budget_dialog)
        category_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(budget_dialog, text="Budget Limit:").grid(row=1, column=0, padx=5, pady=5)
        budget_limit_entry = ttk.Entry(budget_dialog)
        budget_limit_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(budget_dialog, text="Spent:").grid(row=2, column=0, padx=5, pady=5)
        spent_entry = ttk.Entry(budget_dialog)
        spent_entry.grid(row=2, column=1, padx=5, pady=5)

        # Load existing values into entry widgets
        values = self.budget_tree.item(selected_item, 'values')[1:]
        category_entry.insert(0, values[0])
        budget_limit_entry.insert(0, values[1])
        spent_entry.insert(0, values[2])

        # Function to save the edited budget entry
        def save_edited_budget():
            new_category = category_entry.get()
            new_budget_limit = float(budget_limit_entry.get())
            new_spent = float(spent_entry.get())

            # Update the database with edited budget entry details
            query = "UPDATE budgets SET category = %s, budget_limit = %s, spent = %s WHERE id = %s"
            cur.execute(query, (new_category, new_budget_limit, new_spent, item_id))
            conn.commit()

            # Reload budgets after editing
            self.load_budgets()
            budget_dialog.destroy()

        # Button to save the edited budget entry
        ttk.Button(budget_dialog, text="Save", command=save_edited_budget).grid(row=3, columnspan=2, padx=5, pady=10)

    def export_report(self):
        # Function to export the generated report to a text file
        filename = "financial_report.txt"
        with open(filename, "w") as file:
            file.write(self.report_text.get("1.0", tk.END))
        messagebox.showinfo("Success", f"Report has been exported to {filename}")

    def generate_report(self):
        # Function to generate financial report
        report_text = "Financial Report\n\n"
        # Fetch total expenses
        cur.execute("SELECT SUM(amount) FROM expenses")
        total_expenses = cur.fetchone()[0]
        if total_expenses is None:
            total_expenses = 0
        report_text += f"Total Expenses: ${total_expenses}\n"
        # Fetch total income
        cur.execute("SELECT SUM(amount) FROM income")
        total_income = cur.fetchone()[0]
        if total_income is None:
            total_income = 0
        report_text += f"Total Income: ${total_income}\n"
        # Calculate balance
        balance = total_income - total_expenses
        report_text += f"Balance: ${balance}\n\n"
        # Display the report in the Text widget
        self.report_text.delete(1.0, tk.END)  # Clear previous content
        self.report_text.insert(tk.END, report_text)
        # Enable export button
        self.export_button.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalFinanceTracker(root)
    root.mainloop()

# Close PostgreSQL Database Connection
cur.close()
conn.close()
