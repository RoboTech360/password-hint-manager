# project: local password hint manager
# GitHub: https://github.com/RoboTech360
# description: this program is a simple local password manager for storing and retrieving password hints.
#              it uses a master password for access, and the hints are stored in a local SQLite database.
#              the program includes basic functionality for adding, updating, retrieving, and deleting password hints.
# author: RoboTech360

import os
import logging
import login  # import the login module
import passwd_hint  # import the password hint module

# // loggin setup 04/05/2025
log_file= os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log.txt')

logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
# //
# this is where it all starts...!
# check if the master password is set by trying to load it
if not login.load_master_password():  # if no master password is set
    login.set_master_password()  # prompt the user to set the master password
else:
    login.login_window()  # show the login window if master password is already set
