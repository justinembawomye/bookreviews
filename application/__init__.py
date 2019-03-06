
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required, LoginManager

# local import
from instance.config import app_config
from flask import render_template, redirect, url_for, flash
from .forms import RegistrationForm, LoginForm, SearchForm



# initialize sql-alchemy
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

from .models import User, Book

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    bcrypt.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    @app.route('/')
    def index():
        books = Book.query.all()
        return render_template('index.html')


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
        logout_user 
        return render_template('index.html') 


    @app.route('/books', methods=['POST', 'GET'])
    @login_required
    def books():
        form = SearchForm()
        books=Book.query.all()
        message = None
        if form.validate_on_submit():
            results = form.content.data
            books = Book.query.filter((Book.isbn.contains(results)) | (Book.title.contains(results)) | (Book.author.contains(results)) | (Book.year.contains(results)))
            if not books:
                message = "No books found"
                return render_template('error.html', message=message)
           # return render_template('results.html', books=books)
        return render_template('books.html', form=form, books=books)

    @app.route("/book/<int:book_id>", methods=['GET', 'POST'])
    @login_required
    def book(book_id):
        response = Book.query.filter_by(id=book_id).first()
        return render_template('book_details.html',response=response)
  
    return app
