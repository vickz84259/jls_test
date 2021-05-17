from flask import Flask, render_template

import db

app = Flask(__name__)


@app.route('/')
def index():
    with db.get_db() as database:
        products = database.execute(
            'SELECT core_number, internal_title FROM products')

        return render_template('index.html', products=products)


def init_app(app: Flask) -> None:
    with app.app_context():
        db.init_db()

    app.teardown_appcontext(db.close_db)


if __name__ == '__main__':
    init_app(app)
    app.run(debug=True)
