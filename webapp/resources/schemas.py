from marshmallow import Schema, fields, ValidationError, validates_schema, post_load
from webapp.resources.models import check_if_book_with_given_title_and_author_exists, Book


class BookSchema(Schema):
    # TODO: надо разобраться с тем, как получать id,
    #   по идее они должны генерироваться автоматически,
    #   как в при добавлении записи в таблицу
    #   id = fields.Int(dump_only=True)
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)

    @validates_schema
    def validate_title_author_combination(self, data, **kwargs) -> None:
        title = data['title']
        author = data['author']
        if check_if_book_with_given_title_and_author_exists(title, author):
            raise ValidationError('Book with title "{}" by {} already exists,'
                                  ' please, use a different combination;'.format(title, author))

    @post_load
    def create_book(self, data, **kwargs) -> Book:
        return Book(**data)
