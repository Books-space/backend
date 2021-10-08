from flask_testing import TestCase
from app import app
from webapp.resources.models import force_recreate_mock_db

BOOK_LIST_RESOURCE_URL = '/api/v1/book/'

EXPECTED_BOOK_LIST_RESPONSE = [{'id': 1, 'title': 'A Byte Of Python', 'author': 'Swaroop C. H.'},
                               {'id': 2, 'title': 'Грокаем Алгоритмы', 'author': 'Адитья Бхаргава'},
                               {'id': 3, 'title': 'Карьера Программиста', 'author': 'Г. Лакман Макдауэлл'}]

TEST_BOOK_ID = '4'

TEST_BOOK_JSON = '''{"id": 4,
"title": "Gospel of Mark",
"author": "Saint Mark"
}'''


class TestBookSpaceBackend(TestCase):

    def create_app(self):
        # TODO: То что для тестов макетная база данных пересоздаётся с нуля - не совсем правильно,
        #  это нужно как-то переработать: как правильно проверять выдачу списка книг? Как-то переключать всё приложение
        #  на другую тестовую базу данных?
        force_recreate_mock_db()

        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        return app

    '''
    Testing RESTful Resources:
    '''

    def test_book_list_get_request(self):
        response = self.client.get(BOOK_LIST_RESOURCE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), EXPECTED_BOOK_LIST_RESPONSE)

    def test_book_list_post_and_specific_book_delete_requests(self):
        # Add new book
        response = self.client.post(BOOK_LIST_RESOURCE_URL, data=TEST_BOOK_JSON, content_type='application/json')
        self.assertEqual(201, response.status_code)

        # Try to add the same new book
        response = self.client.post(BOOK_LIST_RESOURCE_URL, data=TEST_BOOK_JSON, content_type='application/json')

        self.assertEqual(400, response.status_code)

        # The list of books must be different from original
        response = self.client.get(BOOK_LIST_RESOURCE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json(), EXPECTED_BOOK_LIST_RESPONSE)

        # Delete new book
        response = self.client.delete(BOOK_LIST_RESOURCE_URL + TEST_BOOK_ID)
        self.assertEqual(204, response.status_code)

        # The list must be the same as original
        response = self.client.get(BOOK_LIST_RESOURCE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), EXPECTED_BOOK_LIST_RESPONSE)

    # TODO: ещё нужны тесты для get и put отдельной книги