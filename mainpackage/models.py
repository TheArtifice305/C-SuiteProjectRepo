from mainpackage import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


# class RolesUsers(mainpage.db.Model):
#     __tablename__ = 'roles_users'
#     id = mainpage.db.Column(mainpage.db.Integer(), primary_key=True)
#     user_id = mainpage.db.Column('user_id', mainpage.db.Integer(), mainpage.db.ForeignKey('users.user_id'))
#     role_id = mainpage.db.Column('role_id', mainpage.db.Integer(), mainpage.db.ForeignKey('role.role_id'))
#
#
# class Role(mainpage.db.Model):
#     __tablename__ = 'role'
#     role_id = mainpage.db.Column(mainpage.db.Integer(), primary_key=True)
#     name = mainpage.db.Column(mainpage.db.Text(100), unique=True)

# student = mainpage.Role(name="student")
# admin = mainpage.Role(name="admin")
# community_partner = mainpage.Role(name="community_partner")



# def create_roles():
#     student = mainpage.Role(name="student")
#     admin = mainpage.Role(name="admin")
#     community_partner = mainpage.Role(name="community_partner")
#     mainpage.db.session.add(student, admin, community_partner)
#     mainpage.db.commit()



        # class User(db.Model):
        #     __tablename__ = 'users'
        #     user_id = db.Column(db.Integer, primary_key=True)
        #     username = db.Column(db.String(100), nullable=False, unique=True)
        #     password = db.Column(db.Text)
        #     roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))
        # class RolesUsers(db.Model):
        #     __tablename__ = 'roles_users'
        #     id = db.Column(db.Integer(), primary_key=True)
        #     user_id = db.Column('user_id', db.Integer(), db.ForeignKey('users.user_id'))
        #     role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.role_id'))
        #
        # class Role(db.Model):
        #     __tablename__ = 'role'
        #     role_id = db.Column(db.Integer(), primary_key=True)
        #     name = db.Column(db.Text(100), unique=True)


