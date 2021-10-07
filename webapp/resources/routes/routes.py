from flask import Blueprint, request, jsonify, abort, Response
from dataclasses import asdict
from marshmallow import ValidationError
from webapp.resources import models
from webapp.resources.schemas import BookSchema

routes = Blueprint('routes', __name__)



def abort_if_specific_book_doesnt_exist(book_id):
    if not models.check_if_book_with_given_id_exists(book_id):
        abort(404, 'Book with id {} doesn\'t exist.'.format(book_id)) # TODO: Экранировал апостроф, но это почему-то не помогло

def process_book(model_function):
    data = request.json
    schema = BookSchema()

    try:
        book = schema.load(data)
    except ValidationError as exc:
        return exc.messages, 400

    book = model_function(book)
    return asdict(book), 201


@routes.route('', methods=['POST', 'GET']) # TODO: При рефакторинге добавились фласковские декораторы
def book_list():
    if request.method == 'GET':
        """
        This is for obtaining the books list
        """
        schema = BookSchema()
        response = schema.dump(models.load_book_list_from_db(), many=True)
        return jsonify(books=response) # TODO: Пришлось добавить jsonify, т.к. ответом не может быть список

    if request.method == 'POST':
        """
        This is for book creation
        """
        return process_book(models.add_book)


@routes.route('<book_id>', methods=['GET', 'DELETE', 'PUT'])
def specific_book(book_id: str):
    if request.method == "GET":
        """
        This is for obtaining specific Book information
        """
        book_id = int(book_id)
        abort_if_specific_book_doesnt_exist(book_id)
        response = asdict(models.load_book_from_db_by_id(book_id))
        return response

    if request.method == 'DELETE':
        """
        This is for Book deletion
        """
        book_id = int(book_id)
        abort_if_specific_book_doesnt_exist(book_id)
        models.delete_book(book_id)
        return '', 204

    if request.method == 'PUT':
        """
        This is endpoint for Book replacement
        """
        abort_if_specific_book_doesnt_exist(book_id)
        return process_book(models.replace_book)