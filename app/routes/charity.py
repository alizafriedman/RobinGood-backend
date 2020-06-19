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


@bp.route('/search')
def charities():
    body = request.json
    charity_id = body['charity_id']
    charity = rd.get(charity_id)
    if charity:
        return charity
    else:
        token = request.headers.get('Authorization')
        req = requests.get('http://data.orghunter.com/v1/charitybasic?user_key=3527271551210ee6dbcb09d5e20c8a41&ein=590774235',
                            headers={'Authorization': token}).content
        charityInfo = json.loads(req)
        info = charityInfo['data']
        ein_number = info['ein']
        name = info['name']
        city = info ['city']
        states = info['state']
        test = 'charity'
        add = rd.set(test, states)
        print(add)
        return str(add)
        
    
