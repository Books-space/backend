from flask import Flask
from flask_restful import Api

from webapp.resources.routes import BookList, SpecificBook
from webapp.resources.models import db, Books


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)

    api = Api(app)
    api.add_resource(BookList, '/api/v1/book/')
    api.add_resource(SpecificBook, '/api/v1/book/<book_id>')

    return app
