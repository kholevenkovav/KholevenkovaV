import flask
from flask_sqlalchemy import SQLAlchemy
import os

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_database.db'
database = SQLAlchemy(app)


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
    # category = database.Column(database.String(80))
    name = database.Column(database.String(80), unique=True, nullable=False)
    price = database.Column(database.Integer, nullable=False)
    description = database.Column(database.Text)
    # rating = database.Column(database.Integer)
    logo = database.Column(database.String(80), unique=True, nullable=False)
    link = database.Column(database.String(80), unique=True, nullable=False)


class ShoppingCart(database.Model):
    shopping_cart_id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('accounts.user_id'), nullable=False)
    user = database.relationship('Accounts', backref=database.backref('shopping_cart', lazy=False))
    item_id = database.Column(database.Integer, database.ForeignKey('items.item_id'), nullable=False)
    item = database.relationship('Items', backref=database.backref('shopping_cart', lazy=False))
    count_of_items = database.Column(database.Integer, nullable=False)
    status_of_item = database.Column(database.String(80), nullable=False)


class Responses(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(80), nullable=False)
    email = database.Column(database.String(80), nullable=False)
    text = database.Column(database.Text)


def get_responses():
    return Responses.query.all()[::-1]


def add_items():
    descr = """Lorem ipsum dolor, sit amet consectetur adipisicing elit. Perferendis, earum
                eveniet quasi, magni itaque
                atque
                beatae vel autem eaque debitis, accusantium nulla adipisci. Minus porro esse non cupiditate.
                Placeat,
                similique.
                Quod, corrupti nulla hic, quam quasi, exercitationem eligendi non provident qui sunt error!
                Necessitatibus
                sit,"""
    ball = Items(name="Шарики с цифрами", price=3000, description=descr, logo="ball.jpg", link="ball")
    balloon = Items(name="Шарики в корзинке", price=1500, description=descr, logo="balloon.jpg", link="balloon")
    beauty = Items(name="Красивые шарики", price=4000, description=descr, logo="beauty.jpg", link="beauty")
    database.session.add(ball)
    database.session.add(balloon)
    database.session.add(beauty)
    database.session.commit()


def get_items(min_price, max_price):
    all_items = Items.query.all()

    items = []
    for i in all_items:
        if int(min_price) <= i.price <= int(max_price):
            items.append(i)
    return items


@app.route('/index')
def main_page():
    return flask.render_template("index.html")


@app.route('/about')
def about():
    return flask.render_template("about.html")


@app.route('/response', methods=['GET', 'POST'])
def responses():
    if flask.request.method == 'POST':
        name = flask.request.form.get('name')
        email = flask.request.form.get('email')
        text = flask.request.form.get('text')
        if name != "" and email != "" and text != "":
            response = Responses(name=name,
                                 email=email,
                                 text=text)
            database.session.add(response)
            database.session.commit()
    return flask.render_template("response.html", responses=get_responses())


@app.route('/catalog')
def catalog():
    min_price = flask.request.args.get('min_price', "0")
    max_price = flask.request.args.get('max_price', "1000000000")
    return flask.render_template("catalog.html", items=get_items(min_price, max_price))


def get_item(link):
    all_items = Items.query.all()
    for i in all_items:
        if i.link == link:
            return i
    return None


@app.route('/item/<item>')
def show_item_page(item):
    return flask.render_template('item_page.html', item=get_item(item))


@app.route('/dest')
def dest():
    return flask.render_template("dest.html")


def check_file():
    return os.path.isfile("new_database.db")


if __name__ == '__main__':
    if not check_file():
        database.create_all()
        add_items()
    app.run(debug=True)
