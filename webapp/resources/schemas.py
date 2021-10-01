from marshmallow import Schema, fields, ValidationError
from marshmallow import validates, post_load
from webapp.resources.models import load_book_list_from_db, Book


class BookSchema(Schema):
    # TODO: надо разобраться с тем, как получать id, по идее они должны генерироваться автоматически,
    #   как в при добавлении записи в таблицу
    #   id = fields.Int(dump_only=True)
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)

    @validates('title')
    def validate_title_and_author_combination(self, title: str) -> None:
        # TODO: Разобраться, как валидировать сочетание нескольких аргументов, т.к. у разных авторов
        # могут быть одноименные произведения;
        if [book for book in load_book_list_from_db() if book.title == title]:
            raise ValidationError('Book with title "{}" already exists,'
                                  ' please use a different title'.format(title))

    @post_load
    def create_book(self, data, **kwargs) -> Book:
        return Book(**data)
