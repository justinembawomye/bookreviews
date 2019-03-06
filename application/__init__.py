from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import login_user
#updating the main application
from application.db_setup import init_db, db_session
from application.forms import BookSearchForm

# local import
from instance.config import app_config
from flask import render_template, redirect, url_for, flash, request
from .forms import RegistrationForm, LoginForm


# initialize sql-alchemy
db = SQLAlchemy()
bcrypt = Bcrypt()

from .models import User, Books

init_db()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    bcrypt.init_app(app)
    db.init_app(app)

    @app.route('/register', methods=['POST', 'GET'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            user = User(username=form.username.data,email=form.email.data, password=hashed_password)
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
                flash(f'Welcome {form.username.data}', 'success')
            else:
                flash("Login failed. Please check email and password", "danger")
        return render_template('login.html', title="Login", form=form)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        search = BookSearchForm(request.form)
        if request.method == 'POST':
            return search_results(search)
        return render_template('index.html', form=search)

    @app.route('/results')
    def search_results(search):
        results = []
        search_string = search.data['search']
        if search.data['search'] == '':
            qry = db_session.query(Title)
            results = qry.all()
        if not results:
            flash('No results found!')
            return redirect('/')
        else:
            # display results
            return render_template('results.html', results=results)
    


    return app
