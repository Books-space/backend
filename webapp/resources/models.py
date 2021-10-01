from pathlib import Path
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

db = SQLAlchemy()


class InitBookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)


INIT_SCHEMA = InitBookSchema()
RESOURCES_PATH = Path(__file__).parent
MOCK_DB_PATH = RESOURCES_PATH / 'mock_db.json'


#  TODO: Спросить у Владимира, правильно ли это называть модели во множественном числе,
#   знаю точно, что в Django, например, точно принято их называть в единственном:
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)


@dataclass
class Book:
    id: int
    title: str
    author: str

    def __repr__(self):
        return '<Book id:{}| "{}" after {}>'.format(self.id, self.title, self.author)


def load_book_list_from_db():
    book_list = []
    # TODO: Надо добавить возможность изменять порядок выдочи (asc / desc)
    for book_rec in Books.query.order_by(Books.title.desc()).all():
        book_list.append(Book(book_rec.id,
                              book_rec.title,
                              book_rec.author))
    return book_list


def load_book_from_db_by_id(book_id):
    book_needed = Books.query.filter(Books.id == book_id).first()
    return Book(book_needed.id, book_needed.title, book_needed.author)


def add_book(given_book: Book):
    """
    Function that adds new book to list of books
    :param given_book:
    :return: book
    """
    # TODO: Можно ли распаковывать объект в объект (как это происходит со словарём, например, через **?
    new_book = Books(id=given_book.id, title=given_book.title, author=given_book.title)
    db.session.add(new_book)
    db.session.commit()

    return given_book


def edit_book_by_id(edited_book: Book, book_id):
    book = Books.query.filter_by(id=book_id).first()
    book.title = edited_book.title
    book.author = edited_book.author
    db.session.commit()

    return edited_book


def delete_book(book_id):
    book_to_delete = Books.query.filter(Books.id == book_id).first()
    db.session.delete(book_to_delete)
    db.session.commit()


def check_if_book_with_given_id_exists_in_list(book_id):
    return Books.query.filter(Books.id == book_id).count() > 0
