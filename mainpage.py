from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from pytz import timezone
from werkzeug.security import check_password_hash, generate_password_hash

mainpage = Flask(__name__)
mainpage.config['SECRET_KEY'] = 'accessplease'


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
mainpage.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db.init_app(mainpage)


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.Text)


class Opportunity(db.Model):
    __tablename__ = 'opportunities'
    opportunity_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(99999), nullable=False)
    datetime = db.Column(db.DateTime)
    occurance = db.Column(db.String(100))

class poster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    posted_by = db.Column(db.String(20), nullable=False, default='N/A')
    posted_on = db.Column(db.DateTime, nullable=False)
    occurance_from = db.Column(db.Text)

    def __repr__(self):
        return self.title


with mainpage.app_context():
    db.create_all()
    db.session.commit()


@mainpage.route('/')
def home():
    return render_template('home.html')


@mainpage.route('/login', methods=['GET', 'POST'])
def login():
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
                user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one()
            except db.exc.NoResultFound:
                error = 'Incorrect username or password. Please try again.'
            else:
                if check_password_hash(user.password, password) is False:
                    error = 'Incorrect username or password. Please try again.'
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
                user = User(username=username, password=generate_password_hash(password))
                db.session.add(user)
                db.session.commit()
            except db.exc.IntegrityError:
                error = f'User {username} is already registered. Please pick a different username.'
            else:
                return redirect(url_for('dashboard'))

        flash(error)

    return render_template('register.html')

@mainpage.route('/posts',  methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['post']
        post_author = request.form['author']
        post_occurance = request.form['occurance_from']
        new_post = poster(title=post_title,
                          content=post_content, posted_by=post_author, posted_on=datetime.now(timezone('US/Eastern')), 
                          occurance_from=post_occurance)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = poster.query.order_by(poster.posted_on).all()
        return render_template('posts.html', posts=all_posts)

@mainpage.route('/post/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['post']
        post_author = request.form['author']
        post_occurance = request.form['occurance_from']
        new_post = poster(title=post_title,
                          content=post_content, posted_by=post_author, posted_on=datetime.now(timezone('US/Eastern')), 
                          occurance_from=post_occurance)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/post')
    else:
        return render_template('new_post.html')

@mainpage.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    to_edit = poster.query.get_or_404(id)
    if request.method == 'POST':
        to_edit.title = request.form['title']
        to_edit.posted_by = request.form['author']
        to_edit.content = request.form['post']
        to_edit.occurance_from = request.form['occurance_from']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=to_edit)

@mainpage.route('/posts/delete/<int:id>')
def delete(id):
    to_delete = poster.query.get_or_404(id)
    db.session.delete(to_delete)
    db.session.commit()
    return redirect('/posts')

if __name__ == "__main__":
    mainpage.run(debug=True)