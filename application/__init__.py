
import os
import requests
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required, LoginManager

# local import
from instance.config import app_config
from flask import render_template, redirect, url_for, flash
from .forms import RegistrationForm, LoginForm, SearchForm, ReviewsForm


# initialize sql-alchemy
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


from .models import User, Book, Reviews

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    bcrypt.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    @app.route('/', methods=['POST', 'GET'])
    def index():
        # form = LoginForm()
        # if form.validate_on_submit():
        #     user = User.query.filter_by(email=form.email.data).first()
        #     if user and bcrypt.check_password_hash(user.password, form.password.data):
        #         login_user(user)
        #         flash(f'Welcome', 'success')
        #         return redirect(url_for('books'))
        #     else:
        #         flash("Login failed. Please check email and password", "danger")
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            user = User(username=form.username.data,
                        email=form.email.data, password=hashed_password)
            user.save()
            flash(f"You have successfully created an account! Please login", 'success')

            return redirect(url_for('login'))
        return render_template('index.html', form=form)

    @app.route('/register', methods=['POST', 'GET'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            user = User(username=form.username.data,
                        email=form.email.data, password=hashed_password)
            user.save()
            flash(f"You have successfully created an account! Please login", 'success')

            return redirect(url_for('login'))
        return render_template('register.html', form=form)

    @app.route('/login', methods=['POST', 'GET'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash(f'Welcome', 'success')
                return redirect(url_for('books'))
            else:
                flash("Login failed. Please check email and password", "danger")
        return render_template('login.html', title="Login", form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/books', methods=['POST', 'GET'])
    @login_required
    def books():
        form = SearchForm()
        books = Book.query.all()
        message = None
        if form.validate_on_submit():
            results = form.content.data
            books = Book.query.filter((Book.isbn.contains(results)) | (Book.title.contains(
                results)) | (Book.author.contains(results)) | (Book.year.contains(results)))
            if not books:
                message = "No books found"
                return render_template('error.html', message=message)
           # return render_template('results.html', books=books)
        return render_template('books.html', form=form, books=books)

    @app.route("/book/<int:book_id>", methods=['GET', 'POST'])
    @login_required
    def book(book_id):
        response = Book.query.filter_by(id=book_id).first()
        no_of_reviews = Reviews.query.filter_by(book_id=book_id).all()
        user_review = Reviews.query.filter_by(
            reviewer=current_user, book_id=book_id).first()
        api_key = os.environ.get('API_KEY')
        form = ReviewsForm()
        if not user_review:
            if form.validate_on_submit():
                review = Reviews(review_text=form.review_text.data,
                                 rating=form.rating.data, book_id=book_id, reviewer=current_user)
                db.session.add(review)
                db.session.commit()
                return redirect(url_for('book', book_id=book_id))
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                           params={"key": api_key, "isbns":response.isbn})
        if res.status_code != 200:
            raise Exception("msg: Request failed.")
        goodreads_reviews = res.json()['books']
        return render_template('book_details.html', goodreads_reviews=goodreads_reviews, response=response, reviews=no_of_reviews, user_review=user_review, form=form)    
        
    @app.route("/api/<isbn>", methods =['GET'])
    def api(isbn):
        book = Book.query.filter_by(isbn=isbn).first()
        if book is None:
            return jsonify({"msg" : "No results found.Please check the isbn"}), 404
        reviews = book.reviews
        review_count = len(reviews)
    
        return jsonify({        
            "title": book.title,
            "author":book.author,
            "publication_year": book.year,
            "isbn_number":book.isbn,
            "review_count":review_count,
            "average_score":5.0
        }),200
    return app
