from flask import Flask, request, render_template
from flask_restful import Api

from resources.routes import BookList, SpecificBook

app = Flask(__name__)
api = Api(app)

api.add_resource(BookList, '/api/v1/book/')
api.add_resource(SpecificBook, '/api/v1/book/<book_id>')

if __name__ == "__main__":
    app.run('127.0.0.1', debug=True)
