import logging
from webapp import db, create_app


def create():
    logger = logging.getLogger(__name__)
    db.create_all(app=create_app())
    logger.debug('tables created')
