# login.py
# roject: local password hint manager
# GitHub: https://github.com/RoboTech360
# description: this module handles the setting of the master password and user login for the password manager.

import os
import hashlib
import json
import logging
import tkinter as tk
from tkinter import messagebox  # for showing message boxes in the GUI
import passwd_hint  # import the password manager module to call main_window() after login

# path to the file where the master password will be stored
# config_file = 'config.json'
config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')


def set_master_password():
    """
    This function creates a window where the user can set their master password.
    The password is hashed before being saved in the `config.json` file.
    """
    def save_password():
        """
        Save the entered password after hashing it and store it in the config.json file.
        If no password is entered, show an error message.
        """
        password = password_entry.get()
        if password:
            # Hash the password before saving (use SHA256 for security)
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            # Save the hashed password in a JSON file (config)
            config = {'master_password': hashed_password}
            with open(config_file, 'w') as f:
                json.dump(config, f)
            messagebox.showinfo("Great!", "Master password has been set successfully!")
            logging.info(f"Master password has been set")
            set_password_window.destroy()  # Close the password setup window
            return True  # Return success
        else:
            messagebox.showerror("Error", "Enter a password first.")
            return False

    # Create a window to set the master password
    set_password_window = tk.Tk()
    set_password_window.title("Set Master Password")
    set_password_window.geometry("300x150")

    label = tk.Label(set_password_window, text="Enter onetime Master Password:", font=("Consolas", 12))
    label.pack(pady=10)
    
    password_entry = tk.Entry(set_password_window, font=("Consolas", 12), show="*")  # 'show' hides the input
    password_entry.pack(pady=5)
    
    button = tk.Button(set_password_window, text="Set Master Password", font=("Consolas", 12), command=save_password)
    button.pack(pady=10)
    
    set_password_window.mainloop()  # Start the GUI event loop

def load_master_password():
    """
    This function loads the hashed master password from the `config.json` file.
    Returns the hashed password if it exists, otherwise returns None.
    """
    if os.path.exists(config_file):  # Check if config file exists
        with open(config_file, 'r') as f:
            config = json.load(f)
            return config.get('master_password')  # Return the master password hash
    return None  # Return None if the config file doesn't exist

def login_window():
    """
    This function creates a login window where the user can enter the master password.
    If the entered password matches the stored password hash, the password manager window opens.
    """
    def check_password():
        """
        This function checks if the entered password matches the stored master password.
        If correct, the login window is closed, and the password manager window opens.
        If incorrect, an error message is shown.
        """
        entered_password = password_entry.get()  # Get the entered password
        saved_password_hash = load_master_password()  # Load the saved master password hash
        
        if saved_password_hash:
            # Hash the entered password and compare with the saved hash
            entered_password_hash = hashlib.sha256(entered_password.encode()).hexdigest()
            if entered_password_hash == saved_password_hash:
                root.withdraw()  # Hide the login window
                logging.info(f"login successful!")
                passwd_hint.main_window()  # Open the password manager window after login
            else:
                messagebox.showerror("Error", "Incorrect password! Try again...")  # Show error for incorrect password
                logging.info(f"unsuccessful login attempt!")
                password_entry.delete(0, tk.END)  # Clear the password field
        else:
            messagebox.showerror("Error", "Master password not set! Please set the password first.")
            set_master_password()  # If no password is set, prompt the user to set it

    # Create the login window
    global root
    root = tk.Tk()  # This will be the login window
    root.title("Login - Master Password")
    root.geometry("300x150")
    
    label = tk.Label(root, text="Login with Master Password:", font=("Consolas", 12))
    label.pack(pady=10)
    
    password_entry = tk.Entry(root, font=("Consolas", 12), show="*")  # 'show' hides the input
    password_entry.pack(pady=5)
    
    button = tk.Button(root, text="Login", font=("Consolas", 12), command=check_password)  # Login button
    button.pack(pady=10)
    
    root.mainloop()  # Start the GUI event loop
