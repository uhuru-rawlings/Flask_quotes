class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:Access@localhost/quotes'
    SECRET_KEY = 'testsecretekey'




class ProdConfig(Config):
    pass

class DevConfig(Config):

    DEBUG = True