from typing import Optional
from flask import Blueprint, request, jsonify, abort, make_response
from dataclasses import asdict, dataclass
from marshmallow import ValidationError
from webapp.resources.schemas import BookSchema
from webapp.repositories.books import BooksRepo

routes = Blueprint('routes', __name__)

repo = BooksRepo()
validator = BookSchema()


def validate():
    data = request.json
    try:
        return validator.load(data)
    except ValidationError as exc:
        return exc.messages, 400


@dataclass
class Author:
    name: str
    books_count: int


@dataclass
class BookModel:
    title: str
    author: Author
    likes: int


@routes.route('<int:uid>', methods=['GET'])
def get_by_id(uid: int):
    if not repo.check_by_id(uid):
        abort(make_response(jsonify(message=f"Book with id {uid} doesn\'t exist."), 404))

    # TODO: author = author_repo.get_by_id(book.author)
    author = Author(name='Пушкин', books_count=127)
    # TODO: likes = books_repo.get_likes(uid)

    book_entity = repo.get_by_id(uid)
    book = BookModel(
        title=book_entity.title,
        author=author,
        likes=3,
    )
    return asdict(book)


@routes.route('', methods=['GET'])
def search():
    order: Optional[str] = request.args.get('order', type=str, default='asc')
    title: Optional[str] = request.args.get('title', type=str, default='')
    author: Optional[str] = request.args.get('author', type=str, default='')
    search_str: Optional[str] = request.args.get('search', type=str, default='')
    desc = order == 'desc'
    if search_str:
        books = repo.find_any_inclusions(desc, search_str)
    else:
        books = repo.search(desc, title, author)
    return jsonify(books)


@routes.route('', methods=['POST'])
def add():
    book = validate()
    book = repo.add(title=book.title, author=book.author)
    return asdict(book), 201


@routes.route('<uid>', methods=['PUT'])
def update(uid: int):
    if not repo.check_by_id(uid):
        abort(make_response(jsonify(message=f"Book with id {uid} doesn\'t exist."), 400))

    book = validate()
    book = repo.update(uid=uid, title=book.title, author=book.author)
    return asdict(book), 200


@routes.route('<uid>', methods=['DELETE'])
def delete(uid: int):
    if not repo.check_by_id(uid):
        abort(make_response(jsonify(message=f"Book with id {uid} doesn\'t exist."), 400))

    repo.delete(uid)
    return '', 204


@routes.route('centry')
def trigger_error():
    division_by_zero = 1 / 0
