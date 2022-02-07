from app import app
from flask import Flask,render_template,redirect, url_for,request,session
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
import smtplib
import urllib.request
from flask import flash
import psycopg2
import psycopg2.extras
from flask_mail import Mail, Message

mail= Mail(app)

UPLOAD_FOLDER = 'static/uploads/'
db = SQLAlchemy(app)
# dbconfig
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
# SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
app.config['SECRET_KEY'] = 'testsecretekey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# mailconfig
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mailsendtests1234@gmail.com'
app.config['MAIL_PASSWORD'] = 'rawlings123456789'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)
login_manager.login_view = 'login'

class registration(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    useremail = db.Column(db.String(100))
    password = db.Column(db.String(300))

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

@login_manager.user_loader
def load_user(user_id):
    return registration.query.get(int(user_id))

@app.route('/')
def index():
    title = "Sign-In"
    return render_template('index.html', title = title)

@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        useremail = request.form['usernames']
        passwords = request.form['userpassword']
        getuser = registration.query.filter_by(useremail = useremail).first()
        if getuser:
            passwordget = getuser.password
            passhash = check_password_hash(passwordget,passwords)
            if passhash:
                login_user(getuser, remember = True)
                return redirect(url_for('dashboard'))
            else:
                return "Wrong password, please try again!"
        
        else:
            return "user with this username dont exist"
    return render_template('login.html')

@app.route('/signup', methods = ['POST','GET'])
def signup():
    if request.method == 'POST':
        usernames = request.form['username']
        useremails = request.form['useremails']
        passwords = request.form['password']
        # send email
        msg = Message('Hello', sender = 'mailsendtests1234@gmail.com', recipients = [useremails])
        msg.body = "Hello thank you for signing up to this page, you can check my blogs at techrollblogs.epizy.com"
        mail.send(msg)
        checkexist = registration.query.filter_by(useremail = useremails).first()
        if checkexist:
            return "useremail already exist, please pick another one"
        else:
            passhashs = generate_password_hash(passwords)
            sends = registration(username = usernames, useremail = useremails, password = passhashs)
            db.session.add(sends)
            db.session.commit()
            return redirect('/')
    return render_template('signup.html')

@app.route('/dashboard', methods = ['POST','GET'])
@login_required
def dashboard():
    message = ""
    if request.method == 'POST':
        author = current_user.useremail
        category = request.form['category']
        pitchmessage = request.form['pitchmessage']

        new_post = posts(author = author,  category = category, posts = pitchmessage)
        db.session.add(new_post)
        commits = db.session.commit()
        if commits:
            message = "Post added succesfully"
        else:
             message = "Error adding your post please try again"
    return render_template('dashboard.html', name = current_user.useremail)

@app.route('/interview')
def interview():
    session['url'] = url_for('interview')
    interviews = posts.query.filter_by(category = 'interview').all()
    for ids in interviews:
        idn = ids.id
    postcomm = comment.query.filter_by(post_id = idn).all()
    
    if postcomm:
        result = postcomm
    else:
        result = "No comment for this post"
    return render_template('interview.html', interviews = interviews, name = current_user.useremail, result = result )
@app.route('/promotion')
def promotion():
    session['url'] = url_for('promotion')
    promotions = posts.query.filter_by(category = 'promotion').all()
    # postcomm = comment.query.filter_by(post_id = promotions.id)
    for ids in promotions:
        idn = ids.id
    postcomm = comment.query.filter_by(post_id = idn).all()
    
    if postcomm:
        result = postcomm
    else:
        result = "No comment for this post"
    return render_template('promotion.html', promotions = promotions, name = current_user.useremail, result = result)
@app.route('/products')
def product():
    session['url'] = url_for('product')
    products = posts.query.filter_by(category = 'products').all()
    # postcomm = comment.query.filter_by(post_id = products.id)
    for ids in products:
        idn = ids.id
    postcomm = comment.query.filter_by(post_id = idn).all()
    
    if postcomm:
        result = postcomm
    else:
        result = "No comment for this post"
    if postcomm:
        result = postcomm
    else:
        result = "No comment for this post"
    return render_template('product.html', products = products,name = current_user.useremail, result = result)
@app.route('/mortivation')
def mortivation():
    session['url'] = url_for('mortivation')
    mortivations = posts.query.filter_by(category = 'mortivation').all()
    # postcomm = comment.query.filter_by(post_id = mortivations.id)
    for ids in mortivations:
        idn = ids.id
    postcomm = comment.query.filter_by(post_id = idn)
    
    if postcomm:
        result = postcomm
    else:
        result = "No comment for this post"
    if postcomm:
        result = postcomm
    else:
        result = "No comment for this post"
    if postcomm:
        result = postcomm
    else:
        result = "No comment for this post"
    return render_template('mortivation.html', mortivations = mortivations, name = current_user.useremail, result = result)

@app.route('/profile')
def profile():
    details = registration.query.filter_by(useremail = current_user.useremail).first()
    post = posts.query.filter_by(author = current_user.useremail).count()
    allposts = posts.query.filter_by(author = current_user.useremail).all()
    return render_template('profile.html', details = details, post = post , allposts = allposts)


@app.route('/likes/<int:id>')
def likes(id):
    like_by = current_user.useremail
    new_like = postlikes(post_id = id, likedby = like_by)

    check_like = postlikes.query.filter_by(post_id = id , likedby = current_user.useremail).first()
    if check_like:
        db.session.delete(check_like)
        db.session.commit()
        return redirect (url_for(('dashboard')))
    else:
        db.session.add(new_like)
        db.session.commit()
        return redirect (url_for(('dashboard')))

@app.route('/comments/<int:id>', methods = ['POST','GET'])
def comments(id):
    if request.method == 'POST':
        post_comm = request.form['postcomment']
        post_id = id

        new_comment = comment(post_id = post_id, comment = post_comm)
        db.session.add(new_comment)
        db.session.commit()
        if 'url' in session['url']:
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('dashboard'))




def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	

@app.route('/uploads', methods=['POST'])
def upload_image():
 if 'file' not in request.files:
	 flash('No file part')
	 return redirect(url_for('profile'))

 file = request.files['file']
 if file.filename == '':
	 flash('No image selected for uploading')
	 return redirect(url_for('profile'))
 if file and allowed_file(file.filename):
     filename = secure_filename(file.filename)
     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
     send_image = userprofile(postby = current_user.useremail, imagename = filename)
     db.session.add(send_image)
     db.session.commit()
     flash("Image upload successfull")
     return redirect(url_for('profile'))
 else:
     flash('Allowed image types are -> png, jpg, jpeg, gif')
     return redirect(url_for('profile'))

@app.route('/showcomments/<int:id>')
def showcomments(id):
    getcomment_with_id = comment.query.filter_by(post_id = id).all()
    getlikes = postlikes.query.filter_by(post_id = id).count()
    getpost = posts.query.filter_by(id = id).first()
    
    results = getcomment_with_id

    return render_template('comments.html', results = results, getpost = getpost, getlikes = getlikes)
