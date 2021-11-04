import os
from flask import Flask
from webapp.resources.models import db
from webapp.resources.routes.routes import routes

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


def create_app():
    app = Flask(__name__)
    sentry_sdk.init(
        dsn="https://3a979e0d2537482faf085872cc1c7e1b@o1060270.ingest.sentry.io/6049872",
        integrations=[FlaskIntegration()]
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.register_blueprint(routes, url_prefix='/api/v1/books/')
    return app
