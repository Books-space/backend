from webapp.resources.models import Book, Books, db
from webapp.tools.db.sql import field_contains, sqlfilter, sqlorder


class BooksRepo:

    def get_by_id(self, uid: int) -> Book:
        book = Books.query.filter(Books.id == uid).first()
        return Book(
            book.id,
            book.title,
            book.author,
            book.publisher,
            book.isbn,
            book.year,
            book.cover,
            book.annotation,
        )

    def search(self, order_desc=False, title: str = None, author: str = None):
        query = Books.query
        query = sqlfilter(query, title=title, author=author)
        query = sqlorder(query, Books.title, order_desc)
        query = sqlorder(query, Books.author, order_desc)
        query = sqlorder(query, Books.id, order_desc)

        return [
            Book(
                book.id,
                book.title,
                book.author,
                book.publisher,
                book.isbn,
                book.year,
                book.cover,
                book.annotation,
            )
            for book in query
        ]

    def find_any_inclusions(self, order_desc=False, search_str: str = None):
        query = Books.query
        title_query = field_contains(query, Books.title, search_str)
        author_query = field_contains(query, Books.author, search_str)
        result_query = title_query.union(author_query)
        result_query = sqlorder(result_query, Books.author, order_desc)
        result_query = sqlorder(result_query, Books.title, order_desc)

        return [
            Book(
                book.id,
                book.title,
                book.author,
                book.publisher,
                book.isbn,
                book.year,
                book.cover,
                book.annotation,
            )
            for book in result_query
        ]

    def add(  # noqa: WPS211
        self,
        id: int,  # noqa: WPS125
        title: str,
        author: str,
        publisher: str,
        isbn: str,
        year: int,
        cover: str,
        annotation: str,
    ) -> Book:
        new_book = Books(
            id=id,
            title=title,
            author=author,
            publisher=publisher,
            isbn=isbn,
            year=year,
            cover=cover,
            annotation=annotation,
        )
        db.session.add(new_book)
        db.session.commit()
        return Book(
            id=new_book.id,
            title=new_book.title,
            author=new_book.author,
            publisher=new_book.publisher,
            isbn=new_book.isbn,
            year=new_book.year,
            cover=new_book.cover,
            annotation=new_book.annotation,
        )

    def update(self, uid: int, title: str, author: str) -> Book:
        book = Books.query.filter_by(id=uid).one()
        book.title = title
        book.author = author
        db.session.commit()
        return Book(
            id=book.id,
            title=book.title,
            author=book.author,
            publisher=book.publisher,
            isbn=book.isbn,
            year=book.year,
            cover=book.cover,
            annotation=book.annotation,
        )

    def delete(self, book_id):
        book_to_delete = Books.query.filter(Books.id == book_id).first()
        db.session.delete(book_to_delete)
        db.session.commit()

    def check_by_id(self, book_id) -> bool:
        return Books.query.filter(Books.id == book_id).count() > 0

    def check_by_title_author(self, title: str, author: str) -> bool:
        query = Books.query
        query = query.filter_by(Books.title == title)
        query = query.filter_by(Books.author == author)
        return query.count() > 0
