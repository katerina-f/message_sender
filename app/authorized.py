# external modules
from flask_httpauth import HTTPBasicAuth
from flask import make_response, jsonify

# project modules
from .config import USER, PASSWORD


auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == USER:
        return PASSWORD
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)
