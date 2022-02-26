# EMAIL MODEL
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from  flask_login import UserMixin


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


db = SQLAlchemy(app)


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)



class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    profile_description = db.Column(db.String)
    followers = db.Column(db.Integer)
    following = db.Column(db.Integer)
    creation_date = db.Column(db.String)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String)
    topic = db.Column(db.String)
    body = db.Column(db.String)




class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)


db.create_all()
