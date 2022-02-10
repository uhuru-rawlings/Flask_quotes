from flask import render_template, request
from . import auth
from werkzeug.security import generate_password_hash,check_password_hash
from flask import render_template,redirect,url_for
from ..models import registration
from .. import db
from flask import flash,request 
from flask_login import login_user, current_user
from flask_login import login_required,logout_user
from ..email import mail_message

@auth.route('/login', methods = ['POST','GET'])
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
                return redirect(request.args.get('next') or url_for('root.dashboard'))
               
            else:
                flash("Wrong password, please try again!")
                return redirect(url_for('auth.login'))
        
        else:
            flash("user with this username dont exist")
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html')



@auth.route('/signup', methods = ['POST','GET'])
def signup():
    if request.method == 'POST':
        usernames = request.form['username']
        useremails = request.form['useremails']
        passwords = request.form['password']
        # send email
        checkexist = registration.query.filter_by(useremail = useremails).first()
        if checkexist:
            flash("useremail already exist, please pick another one")
            return redirect (request.referrer)
        else:
            passhashs = generate_password_hash(passwords)
            sends = registration(username = usernames, useremail = useremails, password = passhashs)
            db.session.add(sends)
            db.session.commit()
            return redirect(url_for('auth.login'))
    return render_template('auth/signup.html')
