import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkinter import Toplevel


def create_tab1(parent_frame):
    def create_database():
        conn = sqlite3.connect('accounts.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def save_credentials(username, password):
        try:
            conn = sqlite3.connect('accounts.db')
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO accounts (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def edit_account(id, username, password):
        conn = sqlite3.connect('accounts.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE accounts SET username = ?, password = ? WHERE id = ?',
                       (username, password, id))
        conn.commit()
        conn.close()

    def delete_account(id):
        conn = sqlite3.connect('accounts.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM accounts WHERE id = ?', (id,))
        conn.commit()
        conn.close()

    def fetch_accounts():
        conn = sqlite3.connect('accounts.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password FROM accounts')
        accounts = cursor.fetchall()
        conn.close()
        return accounts

    def on_submit():
        username = entry_username.get()
        password = entry_password.get()

        if not username or not password:
            messagebox.showerror('Error', 'Please fill in both fields')
            return

        if save_credentials(username, password):
            messagebox.showinfo(
                'Success', 'Account information saved successfully')
            refresh_account_list()
        else:
            messagebox.showerror('Error', 'Username already exists')

    def show_edit_dialog(account_id, username, password):

        def on_edit_submit():
            new_username = edit_entry_username.get()
            new_password = edit_entry_password.get()

            if not new_username or not new_password:
                messagebox.showerror('Error', 'Please fill in both fields')
                return

            edit_account(account_id, new_username, new_password)
            edit_dialog.destroy()
            messagebox.showinfo(
                'Success', 'Account information updated successfully')
            refresh_account_list()

        edit_dialog = Toplevel(parent_frame)
        edit_dialog.title('Edit Account')
        edit_dialog.columnconfigure(1, weight=1)

        edit_label_username = tk.Label(edit_dialog, text='Username:')
        edit_label_username.grid(
            row=0, column=0, padx=(10, 5), pady=(10, 5))

        edit_entry_username = tk.Entry(edit_dialog)
        # Prefill the username field
        edit_entry_username.insert(0, username)
        edit_entry_username.grid(
            row=0, column=1, padx=(5, 10), pady=(10, 5))

        edit_label_password = tk.Label(edit_dialog, text='Password:')
        edit_label_password.grid(
            row=1, column=0, padx=(10, 5), pady=(5, 10))

        edit_entry_password = tk.Entry(edit_dialog, show='*')
        # Prefill the password field
        edit_entry_password.insert(0, password)
        edit_entry_password.grid(
            row=1, column=1, padx=(5, 10), pady=(5, 10))

        edit_submit_button = tk.Button(
            edit_dialog, text='Submit', command=on_edit_submit)
        edit_submit_button.grid(
            row=2, column=0, columnspan=2, pady=(5, 10))

    def on_edit():
        selected_item = account_tree.selection()
        if not selected_item:
            messagebox.showerror(
                'Error', 'Please select an account to edit')
            return

        item_data = account_tree.item(selected_item)
        account_id, username, password = item_data['values']
        show_edit_dialog(account_id, username, password)

    def on_delete():
        selected_item = account_tree.selection()
        if not selected_item:
            messagebox.showerror('Error', 'Please select an account to delete')
            return

        item_data = account_tree.item(selected_item)
        account_id, _, _ = item_data['values']

        delete_account(account_id)
        messagebox.showinfo('Success', 'Account deleted successfully')
        refresh_account_list()

    def refresh_account_list():
        accounts = fetch_accounts()
        account_tree.delete(*account_tree.get_children())
        for account in accounts:
            account_tree.insert('', 'end', values=account)

    create_database()

    # Create and configure a custom style for the Treeview headings
    style = ttk.Style(parent_frame)
    style.configure('Treeview.Heading', font=('TkDefaultFont', 10, 'bold'))

    label_username = tk.Label(parent_frame, text='Username:')
    label_username.grid(row=0, column=0, padx=(10, 5),
                        pady=(10, 5), sticky="w")

    entry_username = tk.Entry(parent_frame)
    entry_username.grid(row=0, column=0, padx=(90, 10),
                        pady=(10, 5), sticky="w")

    label_password = tk.Label(parent_frame, text='Password:')
    label_password.grid(row=1, column=0, padx=(10, 5),
                        pady=(5, 10), sticky="w")

    entry_password = tk.Entry(parent_frame, show='*')
    entry_password.grid(row=1, column=0, padx=(90, 10),
                        pady=(5, 10), sticky="w")

    submit_button = tk.Button(parent_frame, text='Submit', command=on_submit)
    submit_button.grid(row=3, column=0,
                       padx=(10, 10), pady=(5, 5), sticky="w")

    edit_button = tk.Button(
        parent_frame, text='Edit Selected', command=on_edit)
    edit_button.grid(row=3, column=0,
                     padx=(70, 10), pady=(5, 5), sticky="w")

    delete_button = tk.Button(
        parent_frame, text='Delete Selected', command=on_delete)
    delete_button.grid(row=3, column=0, padx=(160, 10),
                       pady=(5, 5), sticky="w")

    # Create Treeview to display accounts
    account_tree = ttk.Treeview(parent_frame, columns=(
        'ID', 'Username', 'Password'), show='headings', selectmode='browse', style='Treeview')
    account_tree.heading('ID', text='ID', anchor='center')
    account_tree.heading('Username', text='Username', anchor='center')
    account_tree.heading('Password', text='Password', anchor='center')
    account_tree.grid(row=5, column=0, columnspan=2,
                      padx=(10, 10), pady=(5, 10), sticky='nsew')

    refresh_account_list()

    # Configure the column weights to make the Treeview expand horizontally
    parent_frame.grid_columnconfigure(0, weight=1)
    parent_frame.grid_columnconfigure(1, weight=1)
    # Configure the row weight to make the Treeview expand vertically
    parent_frame.grid_rowconfigure(5, weight=1)

    # Adjust the width of each column and set the anchor to 'center'
    account_tree.column('ID', width=50, anchor='center')
    account_tree.column('Username', width=150, anchor='center')
    account_tree.column('Password', width=200, anchor='center')
