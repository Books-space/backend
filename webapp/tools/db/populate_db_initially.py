import csv
import logging
from webapp import create_app
from webapp.resources.models import Books, Book, db

logger = logging.getLogger(__name__)


def read_books_from_csv(csv_path='books.csv'):
    books_list = []
    with open(csv_path, mode='r') as input_file:
        reader = csv.reader(input_file)
        _ = next(reader)
        for i, (_, title, author, publisher, year, isbn, cover, annotation) in enumerate(reader):
            book = Book(id=i,
                        title=title,
                        author=author,
                        publisher=publisher,
                        year=year,
                        isbn=isbn,
                        cover=cover,
                        annotation=annotation
                        )
            books_list.append(book)
    return books_list


def populate(books_list):
    total_books = len(books_list)
    for i, book in enumerate(books_list, start=1):
        try:
            book_raw = Books(title=book.title,
                             author=book.author,
                             publisher=book.publisher,
                             year=book.year,
                             isbn=book.isbn,
                             cover=book.cover,
                             annotation=book.annotation
                             )
            db.session.add(book_raw)
            db.session.commit()
            logger.info(f'Book added: {i} of {total_books}')
        except Exception as exc:
            logger.info('Book adding failed:')
            logger.exception(exc)
            db.session.rollback()

    print('"Books space" database population is complete.')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s | %(levelname)s: %(message)s',  # noqa: WPS323
    )
    books_list = read_books_from_csv()
    app = create_app()
    with app.app_context():
        populate(books_list)
