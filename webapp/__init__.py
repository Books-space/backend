import os
from flask import Flask
from webapp.resources.models import db
from webapp.resources.routes.routes import routes

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


def db_is_not_available(e):
    return 'Database is not working now!', 500


def create_app():
    app = Flask(__name__)
    sentry_sdk.init(
        dsn=os.environ['SENTRY_DSN'],
        integrations=[FlaskIntegration()],
        environment=os.environ['SENTRY_ENV']
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_error_handler(500, db_is_not_available)
    db.init_app(app)
    app.register_blueprint(routes, url_prefix='/api/v1/books/')
    return app
