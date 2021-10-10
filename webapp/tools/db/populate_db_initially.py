from webapp import create_app
from webapp.resources.models import Books, db

MOCK_BOOK_LIST = [
    {'title': 'A Byte Of Python', 'author': 'Swaroop C. H.'},
    {'title': 'Грокаем Алгоритмы', 'author': 'Адитья Бхаргава'},
    {'title': 'Карьера Программиста', 'author': 'Г. Лакман Макдауэлл'},
]


def populate():
    for book_dict in MOCK_BOOK_LIST:
        try:
            course = Books(**book_dict)
            db.session.add(course)
            db.session.commit()
            print('Book added')
        except Exception as exc:
            print('Book adding failed:')
            print(exc)
            db.session.rollback()

    print('"Books space" database population is complete.')


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        populate()
