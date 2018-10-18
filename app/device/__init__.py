from flask import Blueprint


bp = Blueprint('device', __name__)


from app.device import routes
