import json
from flask import Blueprint, request
from flask_cors import cross_origin
from ..auth import *
from . import rd
from app.model import db, User
import requests
from app.charities import get_charity_by_id

bp = Blueprint('charities', __name__, url_prefix='/charities')


#error handler
@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

#checks if ein exists in redis, returns if there if not adds info to redis, returns the info retrieved


@bp.route('/<int:charity_id>')
@cross_origin(headers=["Content-Type", "Authorization"])
def charities(charity_id):
    # body = request.json
    # charity_id = body['charity_id']
    charity = json.loads(get_charity_by_id(charity_id).decode('utf-8'))[0]
    # charity = json.dumps(charity)
    print(charity)
    return charity

#fetch one charity for main graph


@bp.route('/single')
@cross_origin(headers=["Content-Type", "Authorization"])
def single():
    charity = get_charity_by_id(112940331)
    return charity

@bp.route('/mini')
@cross_origin(headers=["Content-Type", "Authorization"])
def mini():
    charity1 = json.loads(get_charity_by_id(112940331).decode('utf-8'))
    charity2 = json.loads(get_charity_by_id(112940331).decode('utf-8'))
    charity3 = json.loads(get_charity_by_id(112940331).decode('utf-8'))
    charity4 = json.loads(get_charity_by_id(112940331).decode('utf-8'))
    charities = [charity1, charity2, charity3, charity4]
    
    return {'charities': charities}


    
#for front end search
@bp.route('/search')
@cross_origin(headers=["Content-Type", "Authorization"])
def search():
    token = request.headers.get('Authorization')
    search_term = request.args.get('term')
    req = requests.get(f'http://data.orghunter.com/v1/charitysearch?user_key=3527271551210ee6dbcb09d5e20c8a41&searchTerm={search_term}',
                       headers={'Authorization': token}).content
    charityInfo = json.loads(req.decode('utf-8'))
    info = charityInfo['data']
    charity_id = info[0]['ein']
    charity = get_charity_by_id(charity_id)
    print(charity)
    return charity
