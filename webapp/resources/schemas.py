from marshmallow import Schema, fields, post_load
from webapp.resources.models import Book


class BookSchema(Schema):
    # TODO: надо разобраться с тем, как получать id,
    #   по идее они должны генерироваться автоматически,
    #   как в при добавлении записи в таблицу
    #   id = fields.Int(dump_only=True)
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)

    @post_load
    def create_book(self, data, **kwargs) -> Book:
        return Book(**data)
