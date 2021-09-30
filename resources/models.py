from pathlib import Path
from dataclasses import dataclass
import json
from marshmallow import Schema, fields


class InitBookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)


INIT_SCHEMA = InitBookSchema()
RESOURCES_PATH = Path(__file__).parent
MOCK_DB_PATH = RESOURCES_PATH / 'mock_db.json'

@dataclass
class Book:
    id: int
    title: str
    author: str


def load_book_list_from_db():
    with open(MOCK_DB_PATH, "r") as mock_db_file:
        dict_list = json.load(mock_db_file)
    book_list = []
    for book_dict in dict_list:
        book_list.append(Book(book_dict['id'], book_dict['title'], book_dict['author']))
    return book_list


def save_book_list_to_db(book_list):
    with open(MOCK_DB_PATH, 'w') as mock_db_file:
        json.dump(INIT_SCHEMA.dump(book_list, many=True), mock_db_file)


def add_book(given_book):
    """
    Placeholder function than adds new book to list of books
    :param given_book:
    :return: book
    """
    book_list = load_book_list_from_db()
    book_list.append(given_book)
    save_book_list_to_db(book_list)
    return given_book


def delete_book(book_id):
    book_list = load_book_list_from_db()
    for i, book in enumerate(book_list):
        if book.id == book_id:
            break
    else:
        return
    book_list.pop(i)
    save_book_list_to_db(book_list)


def check_if_book_with_given_id_exists_in_list(book_id):
    book_list = load_book_list_from_db()
    print(book_list)
    return len([book for book in book_list if book.id == book_id]) > 0


# -- Временный раздел ----------------------------------------------------------------------------------
MOCK_BOOK_LIST = [{'id': 1, 'title': 'A Byte Of Python', 'author': 'Swaroop C. H.'},
                  {'id': 2, 'title': 'Грокаем Алгоритмы', 'author': 'Адитья Бхаргава'},
                  {'id': 3, 'title': 'Карьера Программиста', 'author': 'Г. Лакман Макдауэлл'}]


def init_mock_db():
    print('Init mock book db')
    save_book_list_to_db([])
    save_book_list_to_db(MOCK_BOOK_LIST)


if __name__ == "__main__":
    init_mock_db()
