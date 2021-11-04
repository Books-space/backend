from typing import Optional
from flask import Blueprint, request, jsonify, abort, make_response
from dataclasses import asdict
from marshmallow import ValidationError
from psycopg2 import OperationalError
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


@routes.route('<uid>', methods=['GET'])
def get_by_id(uid: int):
    if not repo.check_by_id(uid):
        abort(make_response(jsonify(message=f"Book with id {uid} doesn\'t exist."), 400))

    response = asdict(repo.get_by_id(uid))
    return response


@routes.route('', methods=['GET'])
def search():
    order: Optional[str] = request.args.get('order', type=str, default='asc')
    title: Optional[str] = request.args.get('title', type=str, default='')
    author: Optional[str] = request.args.get('author', type=str, default='')
    search_str: Optional[str] = request.args.get('search', type=str, default='')
    desc = order == 'desc'
    # try:
    if search_str:
        books = repo.find_any_inclusions(desc, search_str)
    else:
        books = repo.search(desc, title, author)
    return jsonify(books)
    # except OperationalError:


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
