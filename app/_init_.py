import json
# from six.moves.urllib.request import urlopen
# from functools import wraps

from flask import Flask, request, jsonify, _request_ctx_stack
from flask_cors import cross_origin, CORS
from flask_redis import FlaskRedis
from jose import jwt
from .routes import home
from .auth import *

from .config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    redis_client = FlaskRedis(app)

    app.register_blueprint(home.bp)

