from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from webapp.resources.routes import BookList, SpecificBook
from webapp.resources.models import init_mock_db_if_not_yet

app = Flask(__name__)
api = Api(app)

# TODO: !!! Перенести значения переменных в config.py
# app.config['SQLALCHEMY_DATABASE_URI'] = \
#     'postgresql://vhmmglmh:yATzjfXYcolcsVJ1Gp2A-ugR1dvaYSsa@hattie.db.elephantsql.com/vhmmglmh'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


api.add_resource(BookList, '/api/v1/book/')
api.add_resource(SpecificBook, '/api/v1/book/<book_id>')

init_mock_db_if_not_yet()

# TODO: Код ниже не выполняется при FLASK_APP=app.py
#  и flask run, наверное нужно зарефакторить под фабрику?

# if __name__ == "__main__":
#     print('Start "Book Space" Backend Flask App')
#     init_mock_db_if_not_yet()
#     app.run('127.0.0.1', debug=True)