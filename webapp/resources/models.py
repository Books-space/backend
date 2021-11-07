from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Books(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150), nullable=True)
    publisher = db.Column(db.String(100), nullable=True)
    isbn = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    cover = db.Column(db.String(150), nullable=False)
    annotation = db.Column(db.String(1500), nullable=True)
    db.UniqueConstraint(isbn)


@dataclass
class Book:
    id: int
    title: str
    author: str
    publisher: str
    isbn: str
    year: int
    cover: str
    annotation: str
