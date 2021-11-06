import http
import pytest

from webapp.resources.models import Book


@pytest.mark.xfail
def test_real_db_book_found(books_creator):
    assert 1 == books_creator


def test_add_book(mocker, client):
    pass


def test_sentry_error_raised(client):
    with pytest.raises(ZeroDivisionError):
        client.get('/api/v1/books/centry')


def test_get_book_by_not_found(mocker, client, fake):
    mocker.patch('webapp.repositories.books.BooksRepo.check_by_id', return_value=False)
    uid = fake.pyint()

    resp = client.get(f'/api/v1/books/{uid}')

    assert resp.status_code == http.HTTPStatus.NOT_FOUND
    assert resp.json == {
        'message': f"Book with id {uid} doesn't exist.",
    }


def test_get_book_by_string_id_not_allowed(client, fake):
    uid = fake.pystr()
    resp = client.get(f'/api/v1/books/{uid}')

    assert resp.status_code == http.HTTPStatus.METHOD_NOT_ALLOWED
    assert resp.json == {
        'message': 'method not allowed'
    }


def test_get_book_by_id_found(mocker, client, fake):
    book_title = fake.pystr()

    mocker.patch('webapp.repositories.books.BooksRepo.check_by_id', return_value=True)
    mocker.patch('webapp.repositories.books.BooksRepo.get_by_id', return_value=Book(
        id=1,
        title=book_title,
        author='Пушкин',
        publisher='',
        isbn='',
        year=0,
        cover='',
        annotation='',
    ))

    resp = client.get('/api/v1/books/1')

    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json == {
        'title': book_title,
        'author': {'books_count': 127, 'name': 'Пушкин'},
        'likes': 3,
    }


@pytest.mark.xfail
def test_search_books(client):
    resp = client.get('/api/v1/books/')
    assert resp.status_code == http.HTTPStatus.OK
