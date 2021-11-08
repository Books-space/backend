import csv
import logging

from webapp import create_app
from webapp.resources.models import Book, Books, db

logger = logging.getLogger(__name__)


def read_books_from_csv(csv_path='books.csv'):
    books_list = []
    with open(csv_path, mode='r') as input_file:
        reader = csv.reader(input_file)
        next(reader)
        for book_id, title, author, publisher, year, isbn, cover, annotation in reader:
            book = Book(
                id=book_id,
                title=title,
                author=author,
                publisher=publisher,
                year=year,
                isbn=isbn,
                cover=cover,
                annotation=annotation,
            )
            books_list.append(book)
    return books_list


def populate(books_list):
    total_books = len(books_list)
    for book_num, book in enumerate(books_list, start=1):
        try:
            book_raw = Books(
                id=book.id,
                title=book.title,
                author=book.author,
                publisher=book.publisher,
                year=book.year,
                isbn=book.isbn,
                cover=book.cover,
                annotation=book.annotation,
            )
            db.session.add(book_raw)
            db.session.commit()
            logger.info(f'Book added: {book_num} of {total_books}')
        except Exception as exc:
            logger.exception("The book with id %s wasn't added into db. The reason is: \n%s" % (
                book.id,
                exc,
            ))
            db.session.rollback()

    logger.info('"Books space" database population is complete.')


def populate_db_from_given_csv(csv_path='books.csv'):
    books_list = read_books_from_csv(csv_path=csv_path)
    app = create_app()
    with app.app_context():
        populate(books_list)
    logger.info('Population of the db ended.')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s | %(levelname)s: %(message)s',  # noqa: WPS323
    )
    populate_db_from_given_csv()
