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
def charities(charity_id):
    # body = request.json
    # charity_id = body['charity_id']
    charity = get_charity_by_id(charity_id)
    # charity = json.dumps(charity)
    return charity

#fetch one charity for main graph


@bp.route('/single')
@cross_origin(headers=["Content-Type", "Authorization"])
def single():
    charity = get_charity_by_id(112940331)
    return charity
    
    
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



