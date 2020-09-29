import json
from flask import Blueprint, request
from flask_cors import cross_origin
from ..auth import *
from . import rd
from app.model import db, User

bp = Blueprint('home', __name__, url_prefix='/')


#Error handler
@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response



@bp.route('/private')
# @cross_origin(headers=["Content-Type", "Authorization"])
# @requires_auth
def privateUser():
    return "private user endpoint"





