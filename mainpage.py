from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

mainpage = Flask(__name__)
db = SQLAlchemy()
mainpage.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
mainpage.config['SECRET_KEY'] = 'accessplease'
db.init_app(mainpage)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


@mainpage.route('/')
def home():
    return render_template('home.html')


@mainpage.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@mainpage.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')


@mainpage.route('/logout', methods=['GET', 'POST'])
def logout():
    return redirect(url_for('login'))


@ mainpage.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


if __name__ == "__main__":
    mainpage.run(debug=True)