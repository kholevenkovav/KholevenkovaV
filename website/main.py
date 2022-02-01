import flask

app = flask.Flask(__name__)


@app.route('/index')
def main_page():
    return flask.render_template("index.html")


@app.route('/about')
def about():
    return flask.render_template("about.html")


@app.route('/response')
def response():
    return flask.render_template("response.html")


@app.route('/catalog')
def catalog():
    return flask.render_template("catalog.html")


@app.route('/ball')
def ball():
    return flask.render_template("ball.html")


@app.route('/balloon')
def balloon():
    return flask.render_template("balloon.html")


@app.route('/dest')
def dest():
    return flask.render_template("dest.html")


if __name__ == '__main__':
    app.run(debug=True)
