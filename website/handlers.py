import flask
from website.models import *
from website.main import app, database


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


@app.route('/item/<item>')
def show_item_page(item):
    return flask.render_template('item_page.html', item=get_item(item))


@app.route('/dest')
def dest():
    return flask.render_template("dest.html")
