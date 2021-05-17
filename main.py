from flask import Flask, render_template, redirect, url_for

import db

app = Flask(__name__)


@app.route('/')
def index() -> str:
    with db.get_db() as database:
        products = database.execute(
            'SELECT core_number, internal_title FROM products')

        return render_template('index.html', products=products)


@app.route('/product/<product_number>')
def display_product(product_number: str) -> str:
    with db.get_db() as database:
        cursor = database.execute(
            'SELECT * FROM products WHERE core_number = ?', (product_number, ))
        product = cursor.fetchone()

        cursor = database.execute(
            'SELECT warehouse, location, quantity FROM locations WHERE '
            'product_code = ?',
            (product_number, ))
        locations = cursor.fetchall()

        totals = {}
        for row in locations:
            warehouse = row['warehouse']
            quantity = row['quantity']

            if type(quantity) == str:
                quantity = int(quantity.replace(',', ''))

            if totals.get(warehouse, None):
                totals[warehouse] += quantity
            else:
                totals[warehouse] = quantity

        return render_template(
            'product.html', product=product, locations=locations,
            totals=totals)


@app.route('/update/<product_number>/<key>/<int:quantity>')
def update_quantity(product_number: str, key: str, quantity: int) -> str:
    with db.get_db() as database:
        warehouse, location = key.split(':')

        database.execute(
            'UPDATE locations SET quantity = ? WHERE warehouse = ? AND '
            'product_code = ? AND location = ?',
            (quantity, warehouse, product_number, location))

    return redirect(url_for('display_product', product_number=product_number))


def init_app(app: Flask) -> None:
    with app.app_context():
        db.init_db()

    app.teardown_appcontext(db.close_db)


if __name__ == '__main__':
    init_app(app)
    app.run(debug=True)
