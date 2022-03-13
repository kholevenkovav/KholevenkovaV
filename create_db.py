import os
from website.models import add_items, add_account
from website.main import database

if not os.path.isfile("new_database.db"):
    database.create_all()
    add_items()
    add_account()
