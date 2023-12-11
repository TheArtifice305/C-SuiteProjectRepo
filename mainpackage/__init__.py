from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from mainpackage.authentication import login_required
from werkzeug.security import generate_password_hash


app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'accessplease'


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db.init_app(app)


student_posts = db.Table('student_posts', db.Column('users_id', db.Integer, db.ForeignKey('users.user_id')),
                         db.Column('posters_id', db.Integer, db.ForeignKey('posters.id')))

community_partner_posts = db.Table('community_partner_posts', db.Column('users_id', db.Integer,
                                                                        db.ForeignKey('users.user_id')),
                                   db.Column('posters_id', db.Integer, db.ForeignKey('posters.id')))


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.Text)
    role = db.Column(db.String)
    joined_posts = db.relationship('Poster', secondary=student_posts, backref='student_posts')
    created_posts = db.relationship('Poster', secondary=community_partner_posts, backref='community_partner_posts')


class Poster(db.Model):
    __tablename__ = 'posters'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted_by = db.Column(db.Integer, db.ForeignKey('users.user_id'))
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
