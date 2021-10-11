from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Books(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)


@dataclass
class Book:
    id: int
    title: str
    author: str

    def __repr__(self):
        return '<Book id:{}| "{}" after {}>'.format(self.id, self.title, self.author)
