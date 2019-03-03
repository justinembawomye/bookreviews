from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import login_user

# local import
from instance.config import app_config
from flask import render_template, redirect, url_for, flash
from .forms import RegistrationForm, LoginForm


# initialize sql-alchemy
db = SQLAlchemy()
bcrypt = Bcrypt()

from .models import User


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

    return app
