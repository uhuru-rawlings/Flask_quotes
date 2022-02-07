from app import app

db_uri = app.config['SQLALCHEMY_DATABASE_URI']
secret_key = app.config['SECRET_KEY']
