from flask import Flask, render_template, url_for, redirect, request, flash, g, session, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from mainpackage.authentication import login_required
from werkzeug.security import generate_password_hash
from datetime import datetime
from pytz import timezone
#app = Flask(__name__)
app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'accessplease'


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.Text)
    role = db.Column(db.String)


class Opportunity(db.Model):
    __tablename__ = 'opportunities'
    opportunity_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(99999), nullable=False)
    datetime = db.Column(db.DateTime)
    occurance = db.Column(db.String(100))


class Poster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    posted_by = db.Column(db.String(20), nullable=False, default='N/A')
    posted_on = db.Column(db.DateTime, nullable=False)
    occurance_from = db.Column(db.Text)

    def __repr__(self):
        return self.title


def create_admin_account():
    new_admin = User(email='admin', password=generate_password_hash('admin'), role='admin')
    try:
        db.session.add(new_admin)
        db.session.commit()
    except db.exc.IntegrityError:
        return None
    else:
        return None


with app.app_context():
    db.create_all()
    db.session.commit()
    from mainpackage import authentication, opportunities, admin
    app.register_blueprint(authentication.bp)
    app.register_blueprint(opportunities.bp)
    app.register_blueprint(admin.bp)
    create_admin_account()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


if __name__ == "__main__":
    app.run(debug=True)