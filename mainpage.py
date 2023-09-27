from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
mainpage = Flask(__name__)


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
