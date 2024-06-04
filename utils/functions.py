import getpass
from terminaltables import AsciiTable
from .databse import User, Entry
import pyperclip
import os

loged_in_user = None

def clear():
    os.system('cls' if os.name == "nt" else 'clear')


def login_user():
    username = input("enter your username: ")
    password = getpass.getpass("enter your password: ")

    try:
        user = User.get(username=username, password=password)
        user.logged_in = True
        user.save()
        global loged_in_user
        loged_in_user = user
        print("you successfully logged in.")
        return True
       
    except User.DoesNotExist:
        print("such user does not exist.")
        return False

def logout_user():
    user = User.get(logged_in=True)
    if user:
        user.logged_in = False
        user.save()
        return True
    else:
        return False


def create_user():
    username = input("enter your username: ")
    password = getpass.getpass("enter your password: ")
    if username and password:
        query = User.select().where(User.username==username)
        if not query.exists():
            User.create(username=username, password=password)
            print("user %s successfully created." %(username))
        else:
            print("a user with this username already exist. please try again.")
    else:
        print("try again.")


def add_entry():
    """ add new """
    global loged_in_user
    title = input("title: ")
    url = input("url: ")
    username = input("username: ")
    password = getpass.getpass("password: ")

    data = {
        "owner": loged_in_user,
        "title": title,
        "url": url,
        "username": username,
        "password": password,
    }
    if data:
        if input("save entry ? [Yn] ").lower() != "n":
            Entry.create(**data)
            print("saved successful")


def view_entries(search_title=None):
    """ view all """
    global loged_in_user
    
    entries = Entry.select().order_by(Entry.title.asc())
    entries = entries.where(Entry.owner == loged_in_user)
    
    if search_title:
        entries = entries.where(Entry.title.contains(search_title))
    
    data = [["id", "owner", "title", "url", "username", "password"]]
    
    for entry in entries:
        lst = []
        lst.append(entry.id)
        lst.append(entry.owner.username)
        lst.append(entry.title)
        lst.append(entry.url)
        lst.append(entry.username)
        lst.append('********')

        data.append(lst)

    table = AsciiTable(data)
    print(table.table)
    
    print('\n' + "=" * 8)
    print("c) copy entry password")
    print("d) delete entry")
    print("q) return to main menu")
    next_action = input("action: ").lower().strip()

    if next_action == 'q':
        print()
    elif next_action == 'd':
        delete_entry()
    elif next_action == 'c':
        get_entry_password()

def search_entries():
    """ search """
    view_entries(input("search title: "))

def delete_entry(id=None):
    """ delete an entry """
    global loged_in_user
    try:
        id = int(input("enter entry id: "))
    except:
        clear()
        print("id must be integer")
        print("try again")
        view_entries()

    if id:
        try:
            entry = Entry.get(id=id, owner=loged_in_user)
            if input("Are you sure ? [yN]").lower() == 'y':
                entry.delete_instance()
                print("entry deleted")
                input()
                clear()
                view_entries()
        except:
            print("there is no entry with id : {}".format(id))
            input()
            clear()
            view_entries()

def get_entry_password(id=None):
    """ copy entry password to clipboard """
    global loged_in_user
    try:
        id = int(input("enter entry id: "))
    except:
        clear()
        print("id must be integer")
        print("try again")
        view_entries()

    if id:
        try:
            entry = Entry.get(id=id, owner=loged_in_user)
            pyperclip.copy(entry.password)
            clear()
            print("entry password is in your clipboard now.")
            print("return to view entries.")
            print("-"*10)
            view_entries()
        except:
            print("there is no entry with id : {}".format(id))
            input()
            clear()
            view_entries()