from website.main import database


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


def get_item(link):
    all_items = Items.query.all()
    for i in all_items:
        if i.link == link:
            return i
    return None
