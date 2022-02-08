from app import app
from flask import render_template, redirect, request, url_for

@app.route('/')
def index():
    title = "Sign-In page"
    return render_template('login.html', title = title)