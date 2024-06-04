import os
from peewee import *

main_path = os.path.dirname(os.path.realpath(__file__))
main_path = main_path[:-5]

db = SqliteDatabase(main_path+'/mypassword.db')

class User(Model):
    username = CharField(unique=True)
    password = CharField()
    logged_in = BooleanField(null=True)

    class Meta:
        database = db


class Entry(Model):
    owner = ForeignKeyField(User, backref="entries")
    title = CharField()
    url = CharField(null=True)
    username = CharField()
    password = CharField()

    class Meta:
        database = db


def initialize():
    db.connect()
    db.create_tables([User, Entry], safe=True)
