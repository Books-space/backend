import logging
from webapp import db, create_app


def create():
    try:
        logger = logging.getLogger(__name__)
        db.create_all(app=create_app())
        logger.debug('tables created')
    except Exception as exc:
        logger.exception('Because of following exception: %s' % exc)

