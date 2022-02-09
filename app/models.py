from . import db
from app import app


class posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.String(200))
    category = db.Column(db.String(100))
    posts = db.Column(db.String(1000))

class comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    post_id = db.Column(db.Integer)
    comment = db.Column(db.String(1000))

class postlikes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    post_id = db.Column(db.Integer)
    likedby = db.Column(db.String(100))

class userprofile(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    postby = db.Column(db.String(100))
    imagename = db.Column(db.String(200))
