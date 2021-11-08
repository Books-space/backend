from dataclasses import asdict
from typing import Optional

from flask import Blueprint, abort, jsonify, make_response, request
from marshmallow import ValidationError

from webapp.repositories.books import BooksRepo
from webapp.resources.schemas import BookSchema

routes = Blueprint('routes', __name__)

repo = BooksRepo()
validator = BookSchema()


def validate():
    data = request.json  # noqa: WPS110
    try:
        return validator.load(data)
    except ValidationError as exc:
        return exc.messages, 400


@routes.route('<uid>', methods=['GET'])
def get_by_id(uid: int):
    if not repo.check_by_id(uid):
        abort(make_response(jsonify(message=f"Book with id {uid} doesn\'t exist."), 400))

    return asdict(repo.get_by_id(uid))


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
    book = repo.add(
        id=book.id,
        title=book.title,
        author=book.author,
        publisher=book.publisher,
        isbn=book.isbn,
        year=book.year,
        cover=book.cover,
        annotation=book.annotation,
    )
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
