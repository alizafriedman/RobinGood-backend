from flask import Blueprint, request
from flask_cors import cross_origin
from ..auth import *
from . import rd

bp = Blueprint('home', __name__, url_prefix='/')


# Error handler
# @bp.errorhandler(AuthError)
# def handle_auth_error(ex):
#     response = jsonify(ex.error)
#     response.status_code = ex.status_code
#     return response


@bp.route('')
def home():
    return rd.get('bahamas')