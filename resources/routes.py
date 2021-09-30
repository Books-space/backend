from flask_restful import Resource, reqparse, abort
from resources import models
from resources.schemas import BookSchema
from dataclasses import asdict
from flask import request
from marshmallow import ValidationError

parser = reqparse.RequestParser()
parser.add_argument('format', type=str, location='args')


def abort_if_specific_book_doesnt_exist(book_id):
    if not models.check_if_book_with_given_id_exists_in_list(book_id):
        abort(404, message="Book with id {} doesn't exist.".format(book_id))


def add_book():
    data = request.json
    schema = BookSchema()

    try:
        book = schema.load(data)
        print()
        print(type(book))
    except ValidationError as exc:
        return exc.messages, 400

    book = models.add_book(book)
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
        response = asdict([book for book in models.load_book_list_from_db() if book.id == book_id][0])
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
        return add_book()
