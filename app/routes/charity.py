import json
from flask import Blueprint, request
from flask_cors import cross_origin
from ..auth import *
from . import rd
from app.model import db, User
import requests

bp = Blueprint('charities', __name__, url_prefix='/charities')


#error handler
@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

#checks if ein exists in redis, returns if there if not adds info to redis, returns the info retrieved


@bp.route('')
def charities():
    body = request.json
    charity_id = body['charity_id']
    charity = rd.get(charity_id)
    if charity:
        return charity
    else:
        token = request.headers.get('Authorization')
        req = requests.get(f'http://data.orghunter.com/v1/charityfinancial?user_key=3527271551210ee6dbcb09d5e20c8a41&ein={charity_id}',
                            headers={'Authorization': token}).content
        requ = requests.get(
            f'http://data.orghunter.com/v1/charitysearch?user_key=3527271551210ee6dbcb09d5e20c8a41&sein={charity_id}',
            headers={'Authorization': token}).content
        charityInfo = json.loads(req)
        charityInfos = json.loads(requ)
        print(charityInfos)
        info = charityInfo['data']
        info_w = charityInfos['data'][0]
        print(info_w)
        charity_id = info['ein']
        name = info['name']
        city = info['city']
        state = info['state']
        zipCode = info['zipCode']
        category = info['nteeClass']
        revenue = info['totrevenue'] or 0
        functionalExpenses = info['totfuncexpns'] or 0
        fundraising = info['grsincfndrsng'] or 0
        contributions = info['totcntrbgfts'] or 0
        url = info_w['url']
        donate = info_w['donationUrl']

        dictionary = {
        'name': name,
        'city': city,
        'state': state,
        'zip code': zipCode,
        'category': category,
        'total revenue': int(revenue),
        'total functional expenses': int(functionalExpenses),
        'gross fundraising': int(fundraising),
        'total contributions': int(contributions),
        'website': url,
        'donate link': donate
        }

        data = json.dumps(dictionary)
        rd.set(charity_id, data)
        result = rd.get(charity_id)
        res = json.loads(result)
        return res

#patch = add multiple charities to user - no post needed bec default value null?


@bp.route('/<int:user_id>', methods=['PATCH'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def add_charity():
    token = request.headers.get('Authorization')
    req = requests.get('https://dev-cv4x5nh5.us.auth0.com/userinfo',
                       headers={'Authorization': token}).content
    userInfo = json.loads(req)
    user = User.query.filter_by(email=userInfo['email']).first()
    data = request.json
    new_list = [*user.charity, data['charity_id']]
    user.charity = new_list
    db.session.commit()
    return 'charity successfully added to your portfolio', 201


#delete a charity from the portfolio

@bp.route('', methods=['DELETE'])
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



#for front end search
@bp.route('/search/')
@cross_origin(headers=["Content-Type", "Authorization"])
def search():
    token = request.headers.get('Authorization')
    search_term = request.args.get('search_term')
    req = requests.get(f'http://data.orghunter.com/v1/charitysearch?user_key=3527271551210ee6dbcb09d5e20c8a41&searchTerm={search_term}',
                       headers={'Authorization': token}).content
    charityInfo = json.loads(req)
    info = charityInfo['data']
    print(info)
    return 'apple'



