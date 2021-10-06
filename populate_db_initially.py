from webapp import create_app
from webapp.resources.models import Books, db

MOCK_BOOK_LIST = [{'id': 1, 'title': 'A Byte Of Python', 'author': 'Swaroop C. H.'},
                  {'id': 2, 'title': 'Грокаем Алгоритмы', 'author': 'Адитья Бхаргава'},
                  {'id': 3, 'title': 'Карьера Программиста', 'author': 'Г. Лакман Макдауэлл'}]


def populate():
    for book_dict in MOCK_BOOK_LIST:
        try:
            course = Books(**book_dict)
            db.session.add(course)
            db.session.commit()
            print('Book added')
        except:
            print('Book adding failed')
            db.session.rollback()

    print('"Books space" database population is complete.')


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        populate()
