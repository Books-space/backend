from flask_restful import Resource, abort
from webapp.resources import models
from webapp.resources.schemas import BookSchema
from dataclasses import asdict
from flask import request
from marshmallow import ValidationError


def abort_if_specific_book_doesnt_exist(book_id):
    if not models.check_if_book_with_given_id_exists_in_list(book_id):
        abort(404, message="Book with id {} doesn't exist.".format(book_id))


def add_book(book_id=None):
    data = request.json
    schema = BookSchema()

    try:
        book = schema.load(data)
    except ValidationError as exc:
        return exc.messages, 400

    if book_id is None:
        book = models.add_book(book)
    else:
        # TODO: id передаётся и через URL, и через тело запроса, нужно оптимизировать
        book = models.edit_book_by_id(book, book_id)
    return asdict(book), 201


class BookList(Resource):
    def get(self):
        """
        This is an endpoint for obtaining the books list
        """
        schema = BookSchema()
        response = schema.dump(models.load_book_list_from_db(), many=True)
        return response

    def post(self):
        """
        This is endpoint for book creation
        """
        return add_book()


class SpecificBook(Resource):
    def get(self, book_id):
        """
        This is and endpoint for obtaining specific Book information
        """
        book_id = int(book_id)
        abort_if_specific_book_doesnt_exist(book_id)
        response = asdict(models.load_book_from_db_by_id(book_id))
        return response

    def delete(self, book_id):
        """
        This is endpoint for Book deletion
        """
        book_id = int(book_id)
        abort_if_specific_book_doesnt_exist(book_id)
        models.delete_book(book_id)
        return '', 204

    def put(self, book_id):
        """
        This is endpoint for Book creation
        """
        # TODO: Пока не понятно как быть с id (дублируется в теле запроса и пути) книги здесь
        #  наверное нужен patch
        return add_book(book_id)
