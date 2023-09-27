from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

mainpage = Flask(__name__)
db = SQLAlchemy(mainpage)
mainpage.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
mainpage.config['SECRET_KEY'] = 'accessplease'

@mainpage.route('/')
def home():
    return render_template('home.html')

@mainpage.route('/login')
def login():
    return render_template('login.html')

@mainpage.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    mainpage.run(debug=True)
