import os
from flask import Flask, jsonify
from webapp.resources.models import db
from webapp.resources.routes.routes import routes
from sqlalchemy.exc import OperationalError
from werkzeug.exceptions import NotFound
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
import logging


def handle_database_error(e):
    return jsonify({'message': 'Database is not available now. Please, try again later.'}), e.code


def handle_request_error(e):
    return jsonify({'message': 'The server is unanble to process this request.'}), e.code


def handle_error(e):
    logging.error(e)
    return jsonify({'message': 'Something went wrong. Try again later, please.'}), 500


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
