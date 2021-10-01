from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from webapp.resources.routes import BookList, SpecificBook
from webapp.resources.models import init_mock_db_if_not_yet, db, Books


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)

    api = Api(app)
    api.add_resource(BookList, '/api/v1/book/')
    api.add_resource(SpecificBook, '/api/v1/book/<book_id>')

    init_mock_db_if_not_yet()

    return app
