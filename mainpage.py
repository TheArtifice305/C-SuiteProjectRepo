from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

mainpage = Flask(__name__)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
mainpage.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db.init_app(mainpage)


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)


class Opportunity(db.Model):
    __tablename__ = 'opportunities'
    opportunity_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(99999), nullable=False)
    datetime = db.Column(db.DateTime)


with mainpage.app_context():
    db.create_all()


@mainpage.route('/')
def home():
    return render_template('home.html')


@mainpage.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = db.execute(username)

        if not username:
            error = "Please enter a username."

        elif not check_password_hash(user['password'], password):
            error = "Please enter a password."

        if error is None:
            try:
                user = User(username = username, password = generate_password_hash(password))
                db.session.add(user)
                db.session.commit()
            except db.IntegrityError:
                error = f'User {username} is already registered. Please pick a different username.'
            else:
                return redirect(url_for('dashboard'))

        flash(error)
    return render_template('login.html')


@mainpage.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')


@mainpage.route('/logout', methods=['GET', 'POST'])
def logout():
    return redirect(url_for('login'))


@mainpage.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = "Please enter a username."

        elif not password:
            error = "Please enter a password."

        if error is None:
            try:
                user = User(username = username, password = generate_password_hash(password))
                db.session.add(user)
                db.session.commit()
            except db.IntegrityError:
                error = f'User {username} is already registered. Please pick a different username.'
            else:
                return redirect(url_for('dashboard'))

        flash(error)

    return render_template('register.html')

@mainpage.route('/post_testing', methods=['GET', 'POST'])
def post():
    return render_template('post_testing.html')

if __name__ == "__main__":
    mainpage.run(debug=True)