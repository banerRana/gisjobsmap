import os
from itsdangerous import URLSafeTimedSerializer
from functools import wraps
from flask import request
from api.auth.models import User

SCRAPE_EMAIL = os.getenv('SCRAPE_USER')


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response_object = {
            'success': False,
            'message': 'Provide a valid auth token.'
        }
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return response_object, 403
        auth_token = auth_header.split(" ")[1]
        resp = User.decode_auth_token(auth_token)
        if isinstance(resp, str):
            response_object['message'] = resp
            return response_object, 401
        user = User.query.filter_by(id=resp).first()
        if not user or not user.active:
            return response_object, 401
        return f(resp, *args, **kwargs)
    return decorated_function


def user_detail(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
    return serializer.dumps(email, salt=os.getenv('SECURITY_PASSWORD_SALT'))


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
    try:
        email = serializer.loads(
            token,
            salt=os.getenv('SECURITY_PASSWORD_SALT'),
            max_age=expiration
        )
    except Exception as e:
        print('confirm token error', e)
        return False
    return email
