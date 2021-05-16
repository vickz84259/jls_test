from flask import Flask

import db

app = Flask(__name__)


def init_app(app: Flask) -> None:
    with app.app_context():
        db.init_db()

    app.teardown_appcontext(db.close_db)


if __name__ == '__main__':
    init_app(app)
    app.run(debug=True)
