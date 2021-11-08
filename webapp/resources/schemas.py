from marshmallow import Schema, fields, post_load

from webapp.resources.models import Book


class BookSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    author = fields.Str(allow_none=True)
    publisher = fields.Str(allow_none=True)
    isbn = fields.Str(required=True)
    year = fields.Int()
    cover = fields.Str()
    annotation = fields.Str(allow_none=True)

    @post_load
    def create_book(self, data, **kwargs) -> Book:  # noqa: WPS110
        return Book(**data)
