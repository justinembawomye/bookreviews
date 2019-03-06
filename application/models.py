import os
import csv
import psycopg2
from application import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,   UserMixin):

    """This class represents the bucketlist table."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_reviews = db.relationship('Reviews',
                              backref='reviewer', lazy=True, cascade="all, delete-orphan")

    def __init__(self, username, email, password):
        """initialize with name."""
        self.username = username
        self.email = email
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"User: {self.username}"


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(120),  nullable=False)
    author = db.Column(db.String(60), nullable=False)
    year = db.Column(db.String(20), nullable=False)
    reviews = db.relationship(
        'Reviews', backref='author', lazy=True, cascade="all, delete-orphan")

    def __init__(self, isbn, title, author, year):
        """initialize with name."""
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Book.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"Book: {self.title}"

    @staticmethod
    def connection():
        b = open('books.csv')
        reader = csv.reader(b)
        for isbn, title, author, year in reader:
            books = Book(isbn=isbn, title=title, author=author, year=year)
            books.save()


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(50))
    review_text = db.Column(db.String(10000), nullable=False)
    rating = db.Column(db.Integer)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __str__(self):
        return f"Reviews: {self.review_text}, {self.rating}"
