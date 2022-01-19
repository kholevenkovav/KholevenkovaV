from flask import Flask
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_database.db'
database = SQLAlchemy(application)


class Accounts(database.Model):
    user_id = database.Column(database.Integer, primary_key=True)
    login = database.Column(database.String(80), unique=True, nullable=False)
    e_mail = database.Column(database.String(80), unique=True, nullable=False)
    password = database.Column(database.String(80), nullable=False)
    points = database.Column(database.Integer)
    address = database.Column(database.String(80), nullable=False)
    date_of_registration = database.Column(database.DateTime)
    date_of_birthday = database.Column(database.Date)

    def __repr__(self):
        return f'{self.login}'


class Items(database.Model):
    item_id = database.Column(database.Integer, primary_key=True)
    category = database.Column(database.String(80))
    name = database.Column(database.String(80), unique=True, nullable=False)
    price = database.Column(database.Integer, nullable=False)
    description = database.Column(database.Text)
    rating = database.Column(database.Integer)


class ShoppingCart(database.Model):
    shopping_cart_id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('accounts.user_id'), nullable=False)
    user = database.relationship('Accounts', backref=database.backref('shopping_cart', lazy=False))
    item_id = database.Column(database.Integer, database.ForeignKey('items.item_id'), nullable=False)
    item = database.relationship('Items', backref=database.backref('shopping_cart', lazy=False))
    count_of_items = database.Column(database.Integer, nullable=False)
    status_of_item = database.Column(database.String(80), nullable=False)

database.create_all()