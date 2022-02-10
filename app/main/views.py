from curses import flash
from datetime import datetime
from flask import render_template,flash,request
from flask import request,abort,url_for,redirect
from ..models import registration, postlikes,posts,comment,userprofile
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash,check_password_hash
from flask import abort
from .. import db
from . import root
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = 'app/static/uploads/'

@root.route('/', methods = ['POST','GET'])
@login_required
def dashboard():
    message = ""
    if request.method == 'POST':
        author = current_user.useremail
        category = request.form['category']
        pitchmessage = request.form['pitchmessage']
        
        new_post = posts(author = author,  category = category, posts = pitchmessage )
        db.session.add(new_post)
        commits = db.session.commit()
        if commits:
            message = "Post added succesfully"
        else:
             message = "Error adding your post please try again"
    return render_template('dashboard.html',  name = current_user.useremail)

@root.route('/interview')
def interview():
    title = "pitch-App | Interview"
    interviews = posts.query.filter_by(category = 'interview').all()
    return render_template('interview.html', title = title,  name = current_user.useremail , interviews = interviews)

@root.route('/products')
def products():
    title = "pitch-App | Products"
    products = posts.query.filter_by(category = 'products').all()
    return render_template('products.html', title = title,  name = current_user.useremail, products = products)

@root.route('/promotion')
def promotion():
    title = "pitch-App | Promotion"
    promotions = posts.query.filter_by(category = 'promotion').all()
    return render_template('promotion.html', title = title,  name = current_user.useremail, promotions = promotions)

@root.route('/motivation')
def motivation():
    title = "pitch-App | Mortivation"
    mortivations = posts.query.filter_by(category = 'mortivation').all()
    return render_template('motivation.html', title = title,  name = current_user.useremail, mortivations = mortivations)


@root.route('/profile')
def profile():
    details = registration.query.filter_by(useremail = current_user.useremail).first()
    post = posts.query.filter_by(author = current_user.useremail).count()
    postall = posts.query.filter_by(author = current_user.useremail).all()
    getimages = userprofile.query.filter_by(postby = current_user.useremail).first()
    if getimages:
         imageurl = getimages.imagename 
         filepath = 'static/uploads/'+ imageurl 
    else:
        filepath = 'static/uploads/default.png' 
    return render_template('profile.html', details = details, post = post , postall = postall ,filepath = filepath)


@root.route('/likes/<int:id>')
def likes(id):
    like_by = current_user.useremail
    new_like = postlikes(post_id = id, likedby = like_by)

    check_like = postlikes.query.filter_by(post_id = id , likedby = current_user.useremail).first()
    if check_like:
        db.session.delete(check_like)
        db.session.commit()
        return redirect (request.referrer)
    else:
        db.session.add(new_like)
        db.session.commit()
        return redirect (request.referrer)

@root.route('/comments/<int:id>', methods = ['POST','GET'])
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
	

@root.route('/uploads', methods=['POST'])
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
     file.save(os.path.join(UPLOAD_FOLDER, filename))

     filenames = filename.rsplit('.', 1)
     fname = filenames[0]
     lname = filenames[1]
     fullnames = fname + "." + lname
     send_image = userprofile(postby = current_user.useremail, imagename = fullnames)
     db.session.add(send_image)
     db.session.commit()
     flash("Image upload successfull")
     return redirect(url_for('root.profile'))
 else:
     flash('Allowed image types are -> png, jpg, jpeg, gif')
     return redirect(url_for('root.profile'))

@root.route('/showcomments/<int:id>')
def showcomments(id):
    getcomment_with_id = comment.query.filter_by(post_id = id).all()
    getlikes = postlikes.query.filter_by(post_id = id).count()
    getpost = posts.query.filter_by(id = id).first()
    
    results = getcomment_with_id

    return render_template('comments.html', results = results, getpost = getpost, getlikes = getlikes)