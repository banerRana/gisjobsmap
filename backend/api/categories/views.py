from flask import Blueprint, jsonify, request, make_response
from flask.views import MethodView

from .models import Category

categories_blueprint = Blueprint('categories', __name__)


class AllAPI(MethodView):
    """
    Categories Resource
    """

    def get(self):
        get_data = request.args
        try:
            search = get_data.get('search')
            queries = [Category.valid == True]
            if search:
                queries.append(Category.name.ilike('%{}%'.format(search)))
            tags = Category.query.filter(*queries).order_by(Category.name).all()
            return make_response(
                jsonify({"success": True,
                         "data": [i.serialize for i in tags]
                         })), 200
        except Exception as e:
            responseObject = {
                'success': False,
                'message': str(e)
            }
            return make_response(jsonify(responseObject)), 501


# define the API resources
all_view = AllAPI.as_view('all_api')

# add Rules for API Endpoints
categories_blueprint.add_url_rule(
    '/all',
    view_func=all_view,
    methods=['GET']
)
