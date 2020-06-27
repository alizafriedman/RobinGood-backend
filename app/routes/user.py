from flask import Blueprint
from flask_cors import cross_origin
from ..auth import *
from app.model import db, User
import requests
from . import rd

bp = Blueprint("users", __name__, url_prefix='/users')


#error handler
@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@bp.route('')
def user():
    return "hellooooooooo"


        

@bp.route('/private')
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def privateUser():
    return "private user endpoint"


@bp.route('', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
def updateUser():

    body = request.json
    print(body)
    # checks if there there is user in db
    db_user = User.query.filter_by(email=body['email']).first()
    if db_user:  # if user exists updates the user's name
        db_user.nickname = body['nickname']
        return jsonify({'userId': db_user.id}), 201
    else:  # no user exists create a new user
        new_user = User(email=body['email'],
                        nickname=body['email']
                        )
        db.session.add(new_user)
        db.session.commit()

    return 'user created', 201


@bp.route('/<int:user_id>')
@requires_auth
def get_user(user_id):
    person = User.query.filter_by(id=user_id).first()
    if person:
        return person.to_dict(), 201
    else:
        return "person not found", 422


#post

@bp.route('/<int:user_id>', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def add_single(user_id):
    token = request.headers.get('Authorization')
    req = requests.get('https://dev-cv4x5nh5.us.auth0.com/userinfo',
                       headers={'Authorization': token}).content
    userInfo = json.loads(req)
    user = User.query.filter_by(email=userInfo['email']).first()
    data = request.json
    new_list = [data['charity_id']]
    user.charity = new_list
    db.session.commit()
    return 'charity successfully added to your portfolio', 201


@bp.route('/sets')
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def find(user_id):
    token = request.headers.get('Authorization')
    req = requests.get('https://dev-cv4x5nh5.us.auth0.com/userinfo',
                       headers={'Authorization': token}).content
    userInfo = json.loads(req)
    user = User.query.filter_by(email=userInfo['email']).first().id
    data = request.json
    new_list = [data['charity_id']]
    user.charity = new_list
    return user.charity





# @bp.route('/sets')
# @cross_origin(headers=["Content-Type", "Authorization"])
# @requires_auth
# def get_sets():
#     # gets decodes userinfo out of token using auth0 api
#     token = request.headers.get('Authorization')
#     req = requests.get('https://codelet-app.auth0.com/userinfo',
#                        headers={'Authorization': token}).content
#     userInfo = json.loads(req)
#     userId = User.query.filter_by(email=userInfo['email']).first().id

#     userInfo = User.query.options(db.joinedload(
#         'sets').joinedload('votes'), db.joinedload('favorites')).get(userId)
#     return userInfo.to_dict(), 200


#patch = add multiple charities to user - no post needed bec default value null?



@bp.route('/<int:user_id>', methods=['PATCH'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def add_charity(user_id):
    token = request.headers.get('Authorization')
    req = requests.get('https://dev-cv4x5nh5.us.auth0.com/userinfo',
                       headers={'Authorization': token}).content
    userInfo = json.loads(req)
    user = User.query.filter_by(email=userInfo['email']).first()
    data = request.json
    print(data)
    new_list = [*user.charity, data['charity_id']]
    user.charity = new_list
    db.session.commit()
    return 'charity successfully added to your portfolio', 201


#delete a charity from the portfolio

@bp.route('/<int:user_id>', methods=['DELETE'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def delete_charity():
    token = request.headers.get('Authorization')
    req = requests.get('https://dev-cv4x5nh5.us.auth0.com/userinfo',
                       headers={'Authorization': token}).content
    userInfo = json.loads(req)
    user = User.query.filter_by(email=userInfo['email']).first()
    data = request.json
    updated_list = [x for x in user.charity]
    updated_list.remove(data['charity_id'])
    user.charity = updated_list
    db.session.commit()
    return 'delete was successful', 201
