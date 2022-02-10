from logging import root
from flask import Blueprint
root = Blueprint('root', __name__,)
from . import views, errors