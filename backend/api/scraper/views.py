from flask import request, jsonify, make_response
from flask.views import MethodView
from api.auth.util import authenticate, user_detail

from .models import Invalid, Status
from api import db
from flask import Blueprint

scraper_blueprint = Blueprint('scraper', __name__)


class InvalidAPI(MethodView):
    """
    Add Invalid Indeed Keys
    """

    def post(self, user_id):
        try:
            user = user_detail(user_id)
            if not user.admin:
                response_object = {
                    'success': False,
                    'message': 'User {} does not have access to this resource.'.format(user.email)
                }
                return make_response(jsonify(response_object)), 401
            post_data = request.get_json()
            Invalid.bulk_add(keys=post_data.get('keys'))
            responseObject = {
                'success': True,
                'message': 'Successfully added Invalid Keys.',
            }
            return make_response(jsonify(responseObject)), 200

        except Exception as e:
            responseObject = {
                'success': False,
                'message': 'Some error occurred. {}'.format(str(e))
            }
            return make_response(jsonify(responseObject)), 500

    def get(self, user_id):
        try:
            user = user_detail(user_id)
            if not user.admin:
                response_object = {
                    'success': False,
                    'message': 'User {} does not have access to this resource.'.format(user.email)
                }
                return make_response(jsonify(response_object)), 401
            keys = db.session.query(Invalid.key).all()
            responseObject = {
                'success': True,
                'keys': [k[0] for k in keys],
            }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            responseObject = {
                'success': False,
                'message': str(e)
            }
            return make_response(jsonify(responseObject)), 500


class StatusAPI(MethodView):

    def post(self, user_id):

        # post_data = request.form
        try:
            user = user_detail(user_id)
            if not user.admin:
                response_object = {
                    'success': False,
                    'message': 'User {} does not have access to this resource.'.format(user.email)
                }
                return make_response(jsonify(response_object)), 401
            data = request.get_json()
            new_status = Status(**data)
            db.session.add(new_status)
            db.session.commit()
            responseObject = {
                'success': True,
                'message': 'Successfully added new Status.',
            }
            return make_response(jsonify(responseObject)), 200

        except Exception as e:
            responseObject = {
                'success': False,
                'message': 'Some error occurred. {}'.format(str(e))
            }
            return make_response(jsonify(responseObject)), 500


# define the API resources
invalid_view = InvalidAPI.as_view('invalid_api')
status_view = StatusAPI.as_view('status_api')

# add Rules for API Endpoints
scraper_blueprint.add_url_rule(
    '/invalid',
    view_func=authenticate(invalid_view),
    methods=['POST', 'GET']
)
scraper_blueprint.add_url_rule(
    '/status',
    view_func=authenticate(status_view),
    methods=['POST', 'GET']
)
