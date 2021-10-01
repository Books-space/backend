from marshmallow import Schema, fields, ValidationError, validates, validates_schema, post_load
from webapp.resources.models import check_if_book_with_given_title_and_author_exists, Book


class BookSchema(Schema):
    # TODO: надо разобраться с тем, как получать id, по идее они должны генерироваться автоматически,
    #   как в при добавлении записи в таблицу
    #   id = fields.Int(dump_only=True)
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)

    # @validates('title')
    # def validate_title_and_author_combination(self, title: str) -> None:
    #     # TODO: Разобраться, как валидировать сочетание нескольких аргументов, т.к. у разных авторов
    #     #   могут быть одноименные произведения;
    #     if check_if_book_with_given_title_exists_in_list(title):
    #         raise ValidationError('Book with title "{}" already exists,'
    #                               ' please use a different title'.format(title))

    @validates_schema
    def validate_title_author_combination(self, data, partial, many) -> None:
        print('VALIDATION')
        print(data)
        title = data['title']
        author = data['author']
        print(title)
        print(author)
        if check_if_book_with_given_title_and_author_exists(title, author):
            print('EXCEPTION')
            raise ValidationError('Book with title "{}" by {} already exists,'
                                  ' please, use a different combination;'.format(title, author))

    @post_load
    def create_book(self, data, **kwargs) -> Book:
        print(data)
        return Book(**data)
