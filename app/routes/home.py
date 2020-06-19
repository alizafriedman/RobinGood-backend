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


@bp.route('')
def user():
    return "get user"


@bp.route('/private')
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def privateUser():
    return "private user endpoint"


@bp.route('', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def updateUser():
    body = request.json
    # checks if there there is user in db
    db_user = User.query.filter_by(email=body['email']).first()
    if db_user:  # if user exists updates the user's name
        db_user.nickname = body['nickname']
        return jsonify({'userId': db_user.id}), 201
    else:  # no user exists create a new user
        new_user = User(email=body['email'],
                        nickname=body['nickname']
                        )
        db.session.add(new_user)
        db.session.commit()

        return 'user created', 201
