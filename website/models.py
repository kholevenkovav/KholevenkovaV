from website.main import database
import hashlib
import datetime


class Accounts(database.Model):
    user_id = database.Column(database.Integer, primary_key=True)
    login = database.Column(database.String(80), unique=True, nullable=False)
    e_mail = database.Column(database.String(80), unique=True, nullable=False)
    password = database.Column(database.String(80), nullable=False)
    points = database.Column(database.Integer)
    address = database.Column(database.String(80), nullable=False)
    date_of_registration = database.Column(database.DateTime)
    date_of_birth = database.Column(database.Date)

    def validate(self, password):
        return self.password == hashlib.md5(password.encode("utf8")).hexdigest()

    def set_password(self, password):
        self.password = hashlib.md5(password.encode('utf8')).hexdigest()


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

    def set_not_active(self):
        self.status_of_item = 'ordered'


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


def add_account():
    VK = Accounts(
        login="VK",
        e_mail="VK1580@yandex.ru",
        password="",
        points=0,
        address="",
        date_of_registration=datetime.datetime.now(),
        date_of_birth=datetime.datetime.now())
    VK.set_password("1902")
    database.session.add(VK)
    database.session.commit()


def get_item_by_id(id):
    all_items = Items.query.all()
    filtered = list(filter(lambda item: item.item_id == id, all_items))
    return filtered[0] if len(filtered) == 1 else None


def get_shopping_cart_for_user(user_id):
    result = []
    all_cart = ShoppingCart.query.all()
    for c in all_cart:
        if c.user_id == user_id and c.status_of_item == "in shopping cart":
            result.append(c)
    return result


def get_items_from_cart_for_user(user_id):
    result = []
    all_cart = ShoppingCart.query.all()
    for c in all_cart:
        if c.user_id == user_id and c.status_of_item == "in shopping cart":
            result.append(get_item_by_id(c.item_id))
    return result


def get_item_by_link(link):
    all_items = Items.query.all()
    filtered = list(filter(lambda item: item.link == link, all_items))
    return filtered[0] if len(filtered) == 1 else None


def check_item_in_cart(user_id, item_id):
    all_active_items = ShoppingCart.query.all()
    for ai in all_active_items:
        if ai.user_id == user_id and ai.item_id == item_id and ai.status_of_item == "in shopping cart":
            return True
    return False
