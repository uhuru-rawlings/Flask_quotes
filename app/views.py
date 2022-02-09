from flask import render_template, redirect, url_for, request, flash
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import postlikes,postlikes,comment,posts
from app import app
from app import db
import psycopg2
import psycopg2.extras
import urllib.request
import os
from werkzeug.utils import secure_filename
# mail= Mail(app)

UPLOAD_FOLDER = 'static/uploads/'
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)
login_manager.login_view = 'logins'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

class registration(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    useremail = db.Column(db.String(100))
    password = db.Column(db.String(300))

@login_manager.user_loader
def load_user(user_id):
    return registration.query.get(int(user_id))


@app.route('/', methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        useremail = request.form['useremail']
        password = request.form['password']
        getdetails = registration.query.filter_by(useremail = useremail).first()
        passwrds = getdetails.password
        if getdetails:
            checkpass = check_password_hash(passwrds, password)
            if checkpass:
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong password please try again")
        else:
            flash("user with this username dont exist")
    title = "Quote-App login page"
    return render_template('login.html', title= title)
@app.route('/logins')
def logins():
    return render_template('dashboard.html')

@app.route('/signup', methods = ['POST','GET'])
def signup():
    if request.method == 'POST':
        usernames = request.form['usernames']
        useremails = request.form['useremails']
        passwords = request.form['passwords']

        checkexist = registration.query.filter_by(useremail = useremails).first()
        if checkexist:
            return "useremail already exist, please pick another one"
        else:
            passhashs = generate_password_hash(passwords)
            sends = registration(username = usernames, useremail = useremails, password = passhashs)
            db.session.add(sends)
            db.session.commit()
            return redirect('/')
    title = 'Quote-App login page'
    return render_template('signup.html', title = title)

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
            flash("Post added succesfully")
        else:
            flash("Error adding your post please try again")


    return render_template('dashboard.html', name = current_user.useremail)

@app.route('/interview')
def interview():
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
    postall = posts.query.filter_by(author = current_user.useremail).all()
    return render_template('profile.html', details = details, post = post ,postall = postall)


@app.route('/likes/<int:id>')
def likes(id):
    like_by = current_user.useremail
    new_like = postlikes(post_id = id, likedby = like_by)

    check_like = postlikes.query.filter_by(post_id = id , likedby = current_user.useremail).first()
    if check_like:
        db.session.delete(check_like)
        db.session.commit()
        return redirect(request.referrer)
    else:
        db.session.add(new_like)
        db.session.commit()
        return redirect(request.referrer)

@app.route('/comments/<int:id>', methods = ['POST','GET'])
def comments(id):
    if request.method == 'POST':
        post_comm = request.form['postcomment']
        post_id = id

        new_comment = comment(post_id = post_id, comment = post_comm)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(request.referrer)




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