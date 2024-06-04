#!/usr/bin/env python3
from utils.databse import initialize
from utils.functions import (create_user, login_user, add_entry, view_entries, search_entries, logout_user, clear)
from collections import OrderedDict
import sys



def menu_loop():
    """ show the menu """
    choice = None
    while choice != 'q':
        clear()
        print("enter q to quit!")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input("action: ").lower().strip()

        if choice in menu:
            clear()
            menu[choice]()

    if choice == 'q':
        logout = logout_user()
        if logout:
            sys.exit()


def main():
    if 'create-user' in sys.argv:
        create_user()
        sys.exit()

    user_loged_in = login_user()

    if user_loged_in:
        menu_loop()
    else:
        sys.exit()

menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries)
])

if __name__ == "__main__":
    initialize()
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("cancelled by user.")
        sys.exit()
