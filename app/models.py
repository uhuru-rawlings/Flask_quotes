from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager,db

@login_manager.user_loader 
def load_user(user_id):
     return registration.query.get(int(user_id))

class registration(UserMixin,db.Model):
    __tablename__ = 'registration'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    useremail = db.Column(db.String(100))
    password = db.Column(db.String(300))



    def __repr__(self):
        return f'(self.username)'

class posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.String(200))
    category = db.Column(db.String(100))
    posts = db.Column(db.String(1000))

class comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key = True)
    post_id = db.Column(db.Integer)
    comment = db.Column(db.String(1000))

class postlikes(db.Model):
    __tablename__ = 'postlikes'
    id = db.Column(db.Integer, primary_key = True)
    post_id = db.Column(db.Integer)
    likedby = db.Column(db.String(100))

class userprofile(db.Model):
    __tablename__ = 'userprofile'
    id = db.Column(db.Integer, primary_key = True)
    postby = db.Column(db.String(100))
    imagename = db.Column(db.String(200))
