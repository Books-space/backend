import os
from flask import Flask
from resources.models import db
from resources.routes.routes import routes
from tools.db.populate_db_initially import read_books_from_csv, populate


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.register_blueprint(routes)
    return app


if __name__ == '__main__':
    books_list = read_books_from_csv()
    app = create_app()
    db.create_all(app=app)
    with app.app_context():
        populate(books_list)
    app.run(host='0.0.0.0', port=80)
