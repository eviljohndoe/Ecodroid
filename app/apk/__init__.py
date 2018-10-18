from flask import Blueprint

bp = Blueprint('apk', __name__)

from app.apk import routes