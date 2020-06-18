# import json
# from six.moves.urllib.request import urlopen
# from functools import wraps
from flask import Flask, request, jsonify, _request_ctx_stack
from flask_cors import cross_origin, CORS
from .routes import home, rd
# from jose import jwt
# from .auth import *
from .config import Config



app = Flask(__name__)
app.config.from_object(Config)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


app.register_blueprint(home.bp)



rd.init_app(app)

