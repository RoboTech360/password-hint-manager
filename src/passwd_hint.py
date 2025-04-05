# passwd_hint.py
# Project: local password hint manager
# GitHub: https://github.com/RoboTech360
# Description: This module handles the main functionality of the password manager. It allows the user to 
#              add, update, retrieve, and delete password hints stored in a SQLite database.

import os
import shutil
import sqlite3
import tkinter as tk
from tkinter import messagebox
import logging

# path definition for sqlite database
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'passwdhint_vault.db')

def create_database():
    """
    This function creates the SQLite database and table if they don't exist.
    The table stores app names and associated password hints.
    """
    # // for backing up the db file old stuff
    # shutil.copy(db_path, 'passwdhint_vault_backup.db')
    # print("Backup created.")
    # //
    # does db file exist?

    if os.path.exists(db_path):
        try:
            backup_path = db_path.replace('.db', '_backup.db')
            shutil.copy(db_path, backup_path)
            print(f"Backup created: {backup_path}")
            logging.info(f"Backup created: {backup_path}")
        except Exception as e:
            print(f"Failed to create backup: {e}")
            logging.exception(f"Failed to create backup: {e}")
    
    # conn = sqlite3.connect('passwdhint_vault.db') //old test

    try:
        conn = sqlite3.connect(db_path)  # Open the database (or create it)
        c = conn.cursor()
        
        # Create a table for storing app names and hints if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS passwdhint_vault (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        app_name TEXT NOT NULL UNIQUE,
                        hint TEXT NOT NULL)''')  # Added UNIQUE constraint to app_name
        
        conn.commit()  # Commit changes to the database
        conn.close()  # Close the database connection

        print("Database created or connected successfully.")
        logging.info("Database created or connected successfully.")

    except sqlite3.Error as e:
        print(f"Failed to connect to the database: {e}")
        logging.exception(f"Failed to connect to the database: {e}")

def add_or_update_hint(app_name, hint):
    """
    This function adds a new hint or updates an existing one for a specific app.
    If the app name already exists, it asks the user if they want to update the hint.
    """
    conn = sqlite3.connect(db_path)  # Open the database
    c = conn.cursor()
    
    # Check if the app name already exists
    c.execute("SELECT * FROM passwdhint_vault WHERE app_name = ?", (app_name,))
    result = c.fetchone()
    
    if result:  # If the app name already exists
        # Show a confirmation dialog asking if the user wants to update the hint
        response = messagebox.askyesno("Update Hint", f"'{app_name}' already exists. Do you want to update the hint?")
        
        if response:  # If user clicks 'Yes'
            c.execute("UPDATE passwdhint_vault SET hint = ? WHERE app_name = ?", (hint, app_name))
            messagebox.showinfo("Success", f"Hint for '{app_name}' has been updated.")
            logging.warning(f"Updated hint for app: {app_name}")
        else:  # If user clicks 'No'
            messagebox.showinfo("Canceled", "Update operation canceled.")
    else:  # If the app name doesn't exist, insert a new record
        c.execute("INSERT INTO passwdhint_vault (app_name, hint) VALUES (?, ?)", (app_name, hint))
        messagebox.showinfo("Success", f"New hint for '{app_name}' has been added.")
        logging.warning(f"added a hint for app: {app_name}")
    
    conn.commit()  # Commit changes to the database
    conn.close()  # Close the database connection

def get_hint(app_name):
    """
    This function retrieves the hint associated with a specific app.
    Returns the hint if found, otherwise a default message.
    """
    conn = sqlite3.connect(db_path)  # Open the database
    c = conn.cursor()
    
    c.execute("SELECT hint FROM passwdhint_vault WHERE app_name = ?", (app_name,))
    result = c.fetchone()
    
    conn.close()  # Close the database connection

    logging.info(f"fetched hint for app: {app_name}")
    
    return result[0] if result else "No hint available for this app."

def main_window():
    """
    This function creates the main window where the user can manage their password hints.
    It allows the user to add, update, retrieve, and delete hints.
    """
    window = tk.Tk()
    window.title("Password Hint Manager by RoboTech360")
    window.geometry("500x500")  # Set window size
    window.config(bg="#f0f0f0")  # Set background color

    # Set custom font (Consolas)
    font = ("Consolas", 12)

    # Create widgets
    label_app_name = tk.Label(window, text="App Name:", font=font, bg="#f0f0f0")
    label_app_name.grid(row=0, column=0, pady=10, padx=10, sticky="w")

    entry_app_name = tk.Entry(window, font=font, width=30)
    entry_app_name.grid(row=0, column=1, pady=10, padx=10)

    label_hint = tk.Label(window, text="Hint:", font=font, bg="#f0f0f0")
    label_hint.grid(row=1, column=0, pady=10, padx=10, sticky="w")

    # Create a larger text box for hints with a scrollbar
    text_hint = tk.Text(window, font=font, width=30, height=6, wrap=tk.WORD)
    text_hint.grid(row=1, column=1, pady=10, padx=10)

    # Scrollbar for the Text widget
    scrollbar = tk.Scrollbar(window, command=text_hint.yview)
    scrollbar.grid(row=1, column=2, sticky="ns", pady=10)
    text_hint.config(yscrollcommand=scrollbar.set)

    # Buttons
    def retrieve_hint():
        app_name = entry_app_name.get()
        hint = get_hint(app_name)
        # Set the hint directly into the label on the main window, instead of using a pop-up
        label_hint.config(text=f"Hint: {hint}")

    def add_or_update_new_hint():
        app_name = entry_app_name.get()
        hint = text_hint.get("1.0", tk.END).strip()  # Get multi-line input
        if app_name and hint:
            add_or_update_hint(app_name, hint)
            text_hint.delete("1.0", tk.END)  # Clear the hint box after adding or updating
        else:
            messagebox.showerror("Error", "Value in both fields is required!")

    button_retrieve = tk.Button(window, text="Retrieve Hint", font=font, bg="#4CAF50", fg="white", relief="raised", padx=10, command=retrieve_hint)
    button_retrieve.grid(row=2, column=0, columnspan=2, pady=10, padx=10)

    button_add_or_update_hint = tk.Button(window, text="Add or Update Hint", font=font, bg="#008CBA", fg="white", relief="raised", padx=10, command=add_or_update_new_hint)
    button_add_or_update_hint.grid(row=3, column=0, columnspan=2, pady=10, padx=10)

    # Buttons to clear fields and delete app
    def clear_fields():
        entry_app_name.delete(0, tk.END)  # Clear the app name entry field
        text_hint.delete("1.0", tk.END)   # Clear the multi-line text box
        label_hint.config(text="Hint:")    # Clear the displayed hint in the label

        # logging.info(f"cleared all fields")

    def delete_app():
        app_name = entry_app_name.get()
        if app_name:
            response = messagebox.askyesno("Delete App", f"Are you sure you want to delete the hint for '{app_name}'?")
            if response:
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute("DELETE FROM passwdhint_vault WHERE app_name = ?", (app_name,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", f"Hint for '{app_name}' has been deleted.")
                logging.warning(f"deleted hint for app: {app_name}")
                clear_fields()
        else:
            messagebox.showerror("Error", "Please enter an app name to delete.")

    button_clear = tk.Button(window, text="Clear Fields", font=font, bg="#f0ad4e", fg="white", relief="raised", padx=10, command=clear_fields)
    button_clear.grid(row=4, column=0, columnspan=2, pady=10, padx=10)

    button_delete = tk.Button(window, text="Delete App", font=font, bg="#d9534f", fg="white", relief="raised", padx=10, command=delete_app)
    button_delete.grid(row=5, column=0, columnspan=2, pady=10, padx=10)

    # Initialize the database
    create_database()

    window.mainloop()
