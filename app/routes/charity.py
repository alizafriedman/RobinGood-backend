import json
from flask import Blueprint, request
from flask_cors import cross_origin
from ..auth import *
from . import rd
from app.model import db, User
import requests
from app.charities import get_charity_by_id
from flask_restful import reqparse


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
    charity = json.loads(get_charity_by_id(charity_id).decode('utf-8'))[0]

    return charity

#fetch user saved charities from redis


@bp.route('/bulk')
@cross_origin(headers=["Content-Type", "Authorization"])
def bulk_grab():
    data = request.args.getlist('eins[]')
    # print(data)
    bulk_list = rd.mget(data)
    # print(bulk)
    empty = []
    for x in bulk_list:
        b = slice(1, -1)
        empty.append(json.loads(x.decode('utf-8')[b]))
    return {'bulk_list' : empty }

#fetch one charity for main graph


@bp.route('/single')
@cross_origin(headers=["Content-Type", "Authorization"])
def single():
    charity = get_charity_by_id(911914868)
    return charity


#hardcoded four minis from redis


@bp.route('/mini')
@cross_origin(headers=["Content-Type", "Authorization"])
def mini():
    charity1 = json.loads(get_charity_by_id(751835298).decode('utf-8'))[0]
    charity2 = json.loads(get_charity_by_id(530196605).decode('utf-8'))[0]
    charity3 = json.loads(get_charity_by_id(650755522).decode('utf-8'))[0]
    # charity4 = json.loads(get_charity_by_id(113211164).decode('utf-8'))[0]
    # print(charity1)
    charities = [charity1, charity2, charity3]
    
    
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
    # print(charity)
    return charity
