import os
from flask import Flask
from webapp.resources.models import db, Books
from webapp.resources.routes.routes import routes


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URL']
    db.init_app(app)
    app.register_blueprint(routes, url_prefix='/api/v1/book/')
    return app
