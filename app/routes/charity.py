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
        charityInfo = json.loads(req)
        info = charityInfo['data']
        charity_id = info['ein']
        name = info['name']
        city = info['city']
        state = info['state']
        zipCode = info['zipCode']
        category = info['nteeClass']
        revenue = info['totrevenue']
        functionalExpenses = info['totfuncexpns']
        fundraising = info['grsincfndrsng']
        contributions = info['totcntrbgfts']

        dictionary = { 
        'name': name,
        'city': city,
        'state': state,
        'zip code': zipCode,
        'category': category,
        'total revenue': int(revenue),
        'total functional expenses': int(functionalExpenses),
        'gross fundraising': int(fundraising),
        'total contributions': int(contributions)
        }

        data = json.dumps(dictionary)
        rd.set(charity_id, data)
        result = rd.get(charity_id)
        res = json.loads(result)
        db.session.add(str(charity_id))
        db.session.commit()
        print(res)
        return res
    
    
