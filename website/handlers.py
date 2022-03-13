import flask
from website.models import *
from website.main import app, database
import sqlalchemy


@app.route('/')
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


@app.route("/item/<item>", methods=['GET', 'POST'])
def show_item_page(item):
    if flask.request.method == 'POST':
        if flask.session.get('login') is not None:
            user = Accounts.query.filter_by(login=flask.session.get('login'))
            if (user) is not None:
                user = user.one()
                if check_item_in_cart(user.user_id, get_item_by_link(item).item_id):
                    flask.flash('Товар находится в корзине', 'warning')
                else:
                    item2 = ShoppingCart(user_id=user.user_id,
                                         item_id=get_item_by_link(item).item_id,
                                         count_of_items=1,
                                         status_of_item="in shopping cart")

                    database.session.add(item2)
                    database.session.commit()

                    flask.flash('Товар добавлен в корзину', 'success')
                return flask.render_template("item_page.html", item=get_item_by_link(item))

        flask.flash('Пожалуйста, войдите в личный кабинет, чтобы продолжить', 'warning')

    return flask.render_template("item_page.html", item=get_item_by_link(item))


@app.route('/dest')
def dest():
    return flask.render_template("dest.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if flask.request.method == "POST":
        login = flask.request.form.get("login")
        password = flask.request.form.get("password")
        try:
            if Accounts.query.filter_by(login=login).one().validate(password):
                flask.session["login"] = login
                flask.flash(f"Добро пожаловать, {login}!", "success")
                return flask.redirect(flask.url_for("main_page"), code=301)
            flask.flash("Неправильный пароль", "warning")
        except sqlalchemy.exc.NoResultFound:
            flask.flash("Неправильный логин", "danger")

    return flask.render_template("login.html")


@app.route("/logout")
def logout():
    if flask.session.get("login"):
        flask.session.pop("login")
    return flask.redirect("/", code=302)


@app.route('/<login>', methods=['GET', 'POST'])
def profile(login):
    if flask.session.get('login') == login:
        if (Accounts.query.filter_by(login=login)) is not None:
            user = Accounts.query.filter_by(login=login)
            user = user.one()
            if flask.request.method == 'POST':
                old = flask.request.form.get('old_password')
                new = flask.request.form.get('new_password')

                if old == new == None:
                    flask.flash('Заказ оформлен', 'success')

                    cart = get_shopping_cart_for_user(user.user_id)
                    for c in cart:
                        c.set_not_active()
                        database.session.add(c)
                        database.session.commit()
                else:
                    if not user.validate(old):
                        flask.flash('Старый пароль неверный', 'warning')
                    elif old == new:
                        flask.flash('Новый пароль совпадает со старым', 'warning')
                    else:
                        user.set_password(new)
                        flask.flash('Пароль изменен', 'success')
                        database.session.add(user)
                        database.session.commit()

            return flask.render_template('profile.html',
                                         user=user, cart=get_items_from_cart_for_user(user.user_id))

    flask.flash('Пожалуйста, войдите в личный кабинет, чтобы продолжить', 'warning')
    return flask.redirect(flask.url_for('login'), code=301)
