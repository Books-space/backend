import logging
import os

import sentry_sdk
from flask import Flask, jsonify
from sentry_sdk.integrations.flask import FlaskIntegration
from sqlalchemy.exc import OperationalError
from werkzeug.exceptions import NotFound

from webapp.resources.models import db
from webapp.resources.routes.routes import routes


def handle_database_error(error):
    database_error_msg = {'message': 'Database is not available now. Please, try again later.'}
    return jsonify(database_error_msg), error.code


def handle_request_error(error):
    request_error_msg = {'message': 'The server is unanble to process this request.'}
    return jsonify(request_error_msg), error.code


def handle_error(error):
    logging.error(error)
    some_error_msg = {'message': 'Something went wrong. Try again later, please.'}
    return jsonify(some_error_msg), 500


def create_app():
    app = Flask(__name__)
    sentry_sdk.init(
        dsn=os.environ['SENTRY_DSN'],
        integrations=[FlaskIntegration()],
        environment=os.environ['SENTRY_ENV']
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_error_handler(OperationalError, handle_database_error)
    app.register_error_handler(NotFound, handle_request_error)
    app.register_error_handler(Exception, handle_error)
    db.init_app(app)
    app.register_blueprint(routes, url_prefix='/api/v1/books/')
    return app
