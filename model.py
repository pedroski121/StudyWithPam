# EMAIL MODEL
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


db = SQLAlchemy(app)


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    profile_description = db.Column(db.String)
    followers = db.Column(db.Integer)
    following = db.Column(db.Integer)
    creation_date = db.Column(db.String)

    # articles = relationship('Post',back_populates="author")
    # comments = relationship('Comments',back_populates='comment_author')
    profile_picture = relationship('Image', back_populates='user')


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String)
    topic = db.Column(db.String)
    body = db.Column(db.String)
    # date = db.Column(db.String)

    # author_id = db.Column(db.Integer,ForeignKey('user.id'))
    # author = relationship("User",back_populates="articles")

    # comments = relationship('Comments',back_populates='article')

# class Article_Likes(db.Model):
#     id = db.Column(db.Integer)
#     like =
#     user_id = db.Column(db.Integer,ForeignKey('user.id'))
#     user = relationship("User",back_populates='likes')


# class Comments(db.Model):
#     __tablename__ = 'comments'
#     id = db.Column(db.Integer)
#     comments = db.Column(db.String)
#     date = db.Column(db.String)

#     user_id = db.Column(db.Integer,ForeignKey('user.id'))
#     comment_author = relationship('User',back_populates='comments')

#     post_id = db.Column(db.Integer, ForeignKey('user.id'))
#     post = relationship('Post',back_populates='comments')


class Image(db.Model):
    __tablename__ = 'profile_pictures'
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, ForeignKey('user.id'),unique=True)
    user = relationship('User', back_populates='profile_picture')


db.create_all()
