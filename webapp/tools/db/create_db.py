import logging

from webapp import create_app, db


def create():
    logger = logging.getLogger(__name__)
    try:
        db.create_all(app=create_app())
        logger.info('Database and table were created;')
    except Exception:
        logger.exception('The database creation failed.')
