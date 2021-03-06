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


# @bp.route('')
# def user():
#     return "hellooooooooo"


        

@bp.route('/private')
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def privateUser():
    return "private user endpoint"


#Auth0 check / add user to db
@bp.route('', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def updateUser():
    body = request.json
    db_user = User.query.filter_by(email=body['email']).first()
    # print(db_user)
    # print('apple')
    if db_user: 
        db_user.nickname = body['nickname']
        return jsonify({'userId': db_user.id}), 201
    else:  
        new_user = User(email=body['email'],
                        nickname=body['nickname']
                        )
        db.session.add(new_user)
        db.session.commit()
        return {'userId':new_user.id}
    

#find existing user
@bp.route('/<int:user_id>')
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def get_user(user_id):
    person = User.query.filter_by(id=user_id).first()
    if person:
        return person.to_dict(), 201
    else:
        return "person not found", 422


#add charity to user
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
    return 'charity successfully added to your account', 201


#get user saved charities
@bp.route('/<int:user_id>')
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



#patch = add multiple charities to user, or first single
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
    if user.charity:
        print(data)
        new_list = [*user.charity, data['charity_id']]
        user.charity = new_list
        db.session.commit()
        return 'charity successfully added to your portfolio', 201
    else:
        print(data)
        new_list = [data['charity_id']]
        user.charity = new_list
        db.session.commit()
        return 'charity successfully added to your portfolio', 201


#delete a charity from saved
@bp.route('/<int:user_id>', methods=['DELETE'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def delete_charity(user_id):
    token = request.headers.get('Authorization')
    req = requests.get('https://dev-cv4x5nh5.us.auth0.com/userinfo',
                       headers={'Authorization': token}).content
    userInfo = json.loads(req)
    user = User.query.filter_by(email=userInfo['email']).first()
    data = request.json
    updated_list = [*user.charity]
    char = data['charity_id']
    for x in updated_list:
        if int(x) == int(char):
            updated_list.remove(str(x))
            user.charity = updated_list
            db.session.commit()
    return 'delete was successful', 201
