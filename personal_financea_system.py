import pandas as pd
from datetime import datetime
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib
matplotlib.use('TkAgg')


class FinanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personal Finance Management System")
        self.geometry("1300x800")  # Adjusted size for more space

        # Set new theme colors
        self.bg_color = "#e8f5e9"
        self.fg_color = "#004d40"
        self.button_color = "#009688"
        self.entry_bg_color = "#ffffff"
        self.entry_fg_color = "#004d40"
        self.highlight_color = "#ff5722"

        self.configure(bg=self.bg_color)

        # Initialize bank balance
        self.bank_balance = 1000000.00

        # Create SQLite database
        self.conn = sqlite3.connect('finance.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions
                              (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, amount REAL, date TEXT, description TEXT)''')
        self.conn.commit()

        # Create main frame
        main_frame = tk.Frame(self, bg=self.bg_color)
        main_frame.pack(fill='both', expand=True)

        # Create notebook
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)

        # Apply style to the notebook and tabs
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=self.bg_color,
                        foreground=self.fg_color)
        style.map("TNotebook.Tab", background=[
                  ("selected", self.highlight_color)], foreground=[("selected", self.fg_color)])

        # Apply style to Treeview
        style.configure('Treeview',
                        font=('Arial', 12),  # Changed font type and size
                        rowheight=30)  # Increase row height for better visibility

        # Apply style to Combobox
        style.configure('TCombobox',
                        font=('Arial', 14))  # Changed font size for Combobox

        # Create transaction tab
        transaction_tab = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(transaction_tab, text='Transactions')

        # Create transaction widgets
        self.create_label(transaction_tab, 'Type:', 0, 0)
        self.type_var = tk.StringVar()
        self.type_dropdown = ttk.Combobox(transaction_tab, textvariable=self.type_var, values=[
                                          'Income', 'Expense'], font=('Arial', 14))
        self.type_dropdown.grid(
            row=0, column=1, columnspan=2, padx=10, pady=10, sticky='ew')

        self.create_label(transaction_tab, 'Amount:', 1, 0)
        self.amount_entry = self.create_entry(
            transaction_tab, 1, 1, columnspan=2)

        self.create_label(transaction_tab, 'Date:', 2, 0)
        self.date_entry = DateEntry(transaction_tab, font=(
            'Arial', 14), date_pattern='dd-mm-yyyy')
        self.date_entry.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

        self.create_label(transaction_tab, 'Description:', 3, 0)
        self.description_entry = self.create_entry(
            transaction_tab, 3, 1, columnspan=2)

        # Create bank balance widgets
        self.create_label(transaction_tab, 'Bank Balance:', 4, 0)
        self.bank_balance_entry = self.create_entry(
            transaction_tab, 4, 1, columnspan=2)

        update_balance_button = self.create_button(
            transaction_tab, 'Set Balance', self.set_bank_balance, 5, 0, columnspan=2)

        # Create transaction buttons
        add_button = self.create_button(
            transaction_tab, 'Add', self.add_transaction, 6, 0)
        edit_button = self.create_button(
            transaction_tab, 'Edit', self.edit_transaction, 6, 1)
        delete_button = self.create_button(
            transaction_tab, 'Delete', self.delete_transaction, 6, 2)

        # Create Treeview to display transactions
        self.tree = ttk.Treeview(transaction_tab, columns=(
            'ID', 'Type', 'Amount', 'Date', 'Description'), show='headings', height=12)  # Increased height
        self.tree.heading('ID', text='ID')
        self.tree.heading('Type', text='Type')
        self.tree.heading('Amount', text='Amount')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Description', text='Description')
        self.tree.grid(row=7, column=0, columnspan=4,
                       padx=10, pady=10, sticky='nsew')

        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            transaction_tab, orient='vertical', command=self.tree.yview)
        scrollbar.grid(row=7, column=4, sticky='ns')
        self.tree.configure(yscroll=scrollbar.set)

        # Create dashboard tab
        dashboard_tab = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(dashboard_tab, text='Dashboard')

        # Create dashboard widgets
        self.figure, ((self.ax1, self.ax2), (self.ax3, self.ax4)
                      ) = plt.subplots(2, 2, figsize=(16, 12))  # Adjusted size for more space
        self.canvas = FigureCanvasTkAgg(self.figure, master=dashboard_tab)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

        # Create label for total balance
        self.balance_label = tk.Label(dashboard_tab, text=f'Total Balance: ${self.bank_balance:.2f}', font=('Arial', 22, 'bold'),
                                      bg=self.bg_color, fg=self.fg_color)
        self.balance_label.pack(pady=10)

        self.update_dashboard()
        self.update_treeview()

    def create_label(self, parent, text, row, column):
        label = tk.Label(parent, text=text, font=(
            'Arial', 14, 'bold'), bg=self.bg_color, fg=self.fg_color)
        label.grid(row=row, column=column, padx=10, pady=10, sticky='w')
        return label

    def create_entry(self, parent, row, column, columnspan=1):
        entry = tk.Entry(parent, bg=self.entry_bg_color,
                         fg=self.entry_fg_color, font=('Arial', 14))
        entry.grid(row=row, column=column, columnspan=columnspan,
                   padx=10, pady=10, sticky='ew')
        return entry

    def create_button(self, parent, text, command, row, column, columnspan=1):
        button = tk.Button(parent, text=text, command=command, bg=self.button_color, fg=self.fg_color,
                           activebackground=self.highlight_color, font=('Arial', 14, 'bold'))
        button.grid(row=row, column=column, columnspan=columnspan,
                    padx=10, pady=10, sticky='ew')
        return button

    def set_bank_balance(self):
        bank_balance_str = self.bank_balance_entry.get()

        # Validate bank balance input
        try:
            self.bank_balance = float(bank_balance_str)
            self.balance_label.config(
                text=f'Total Balance: ${self.bank_balance:.2f}')
            messagebox.showinfo("Success", "Bank balance set successfully!")
        except ValueError:
            messagebox.showerror(
                "Input Error", "Please enter a valid bank balance.")

    def add_transaction(self):
        transaction_type = self.type_var.get()
        amount_str = self.amount_entry.get()
        date = self.date_entry.get_date().strftime(
            '%d-%m-%Y')
        description = self.description_entry.get()

        # Validate amount input
        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")
            return

        # Update bank balance based on expense
        if transaction_type == 'Expense':
            self.bank_balance -= amount

        # Insert the transaction into the database
        self.cursor.execute("INSERT INTO transactions (type, amount, date, description) VALUES (?, ?, ?, ?)",
                            (transaction_type, amount, date, description))
        self.conn.commit()

        messagebox.showinfo("Success", "Transaction added successfully!")
        self.clear_entries()
        self.update_dashboard()
        self.update_treeview()

    def clean_amount_string(amount_str):
        # Remove any unwanted characters
        return ''.join(c for c in amount_str if c.isdigit() or c == '.')

    def edit_transaction(self):
        selected = self.tree.focus()
        if selected:
            transaction_id = self.tree.item(selected)['values'][0]
            transaction_type = self.type_var.get()
            amount_str = self.amount_entry.get().strip()  # Strip whitespace
            date = self.date_entry.get_date().strftime('%d-%m-%Y')
            description = self.description_entry.get()

            print(f"Amount entered: '{amount_str}'")  # Debugging statement

            if not amount_str:  # This condition should trigger only if amount_str is truly empty
                messagebox.showerror("Input Error", "Amount cannot be empty.")
                return

            try:
                amount = float(amount_str)
            except ValueError:
                messagebox.showerror(
                    "Input Error", "Please enter a valid amount.")
                return

            self.cursor.execute(
                "SELECT amount, type FROM transactions WHERE id = ?", (transaction_id,))
            old_amount, old_type = self.cursor.fetchone()

            if old_type == 'Expense':
                self.bank_balance += old_amount
            if transaction_type == 'Expense':
                self.bank_balance -= amount

            self.cursor.execute(
                "UPDATE transactions SET type = ?, amount = ?, date = ?, description = ? WHERE id = ?",
                (transaction_type, amount, date, description, transaction_id))
            self.conn.commit()

            messagebox.showinfo("Success", "Transaction updated successfully!")
            self.clear_entries()
            self.update_dashboard()
            self.update_treeview()
        else:
            messagebox.showerror(
                "Error", "Please select a transaction to edit.")

    def delete_transaction(self):
        selected = self.tree.focus()
        if selected:
            transaction_id = self.tree.item(selected)['values'][0]

            # Adjust bank balance
            self.cursor.execute(
                "SELECT amount, type FROM transactions WHERE id = ?", (transaction_id,))
            transaction = self.cursor.fetchone()
            if transaction:
                amount, transaction_type = transaction

                # Adjust bank balance if the transaction is an expense
                if transaction_type == 'Expense':
                    self.bank_balance += amount

            # Delete the transaction from the database
            self.cursor.execute(
                "DELETE FROM transactions WHERE id = ?", (transaction_id,))
            self.conn.commit()

            messagebox.showinfo("Success", "Transaction deleted successfully!")
            self.update_dashboard()
            self.update_treeview()
        else:
            messagebox.showerror(
                "Error", "Please select a transaction to delete.")

    def clear_entries(self):
        self.type_dropdown.set('')
        self.amount_entry.delete(0, tk.END)
        self.date_entry.set_date(datetime.now())
        self.description_entry.delete(0, tk.END)

    def update_dashboard(self):
        # Clear previous plots
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax4.clear()

        # Apply new font for graphs
        plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 14})

        # Fetch transactions from the database
        self.cursor.execute("SELECT type, amount, date FROM transactions")
        transactions = self.cursor.fetchall()

        # Calculate total income and expense
        income = sum(amount for ttype, amount,
                     date in transactions if ttype == 'Income')
        expense = sum(amount for ttype, amount,
                      date in transactions if ttype == 'Expense')

        # Set a fallback for empty transactions to prevent NaN issues
        if income == 0 and expense == 0:
            amounts = [1]  # Default value to avoid division by zero
            labels = ["No data available"]
            colors = ['gray']
        else:
            amounts = [income, expense]
            labels = ['Income', 'Expense']
            colors = ['green', 'red']

        # Plot income vs expense pie chart
        self.ax1.pie(amounts, labels=labels, autopct='%1.1f%%',
                     colors=colors, startangle=90)
        self.ax1.set_title('Income vs Expense')

        # Remove the bank balance bar chart
        self.ax2.axis('off')  # Hide the axis for the bank balance plot

        # Remove income and expense trend over time
        self.ax3.axis('off')  # Hide the axis for the income and expense trend

        # Plot category-wise expense distribution as a bar chart
        categories = {}
        for ttype, amount, desc in transactions:
            if ttype == 'Expense':
                category = desc if desc else 'Uncategorized'
                categories[category] = categories.get(category, 0) + amount

        if categories:
            self.ax4.bar(categories.keys(),
                         categories.values(), color='orange')
            self.ax4.set_title('Category-wise Expense Distribution')
            self.ax4.set_xticklabels(
                categories.keys(), rotation=45, ha='right')

        # Update the canvas
        self.canvas.draw()

        # Update the balance label
        self.balance_label.config(
            text=f'Total Balance: ${self.bank_balance:.2f}')

    def update_treeview(self):
        # Clear the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch transactions from the database
        self.cursor.execute("SELECT * FROM transactions")
        transactions = self.cursor.fetchall()

        # Insert transactions into the treeview
        for transaction in transactions:
            self.tree.insert('', 'end', values=transaction)

    def run(self):
        self.mainloop()


# Create and run the finance app
if __name__ == '__main__':
    app = FinanceApp()
    app.run()
