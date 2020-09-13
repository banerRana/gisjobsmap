from flask import Blueprint, jsonify, request, make_response
from flask.views import MethodView
from .models import Tag

tags_blueprint = Blueprint('tags', __name__)


class AllAPI(MethodView):
    """
    Tag Resource
    """

    def get(self):
        get_data = request.args
        try:
            search = get_data.get('search')
            queries = [Tag.valid==True]
            if search:
                queries.append(Tag.name.ilike('%{}%'.format(search)))
            tags = Tag.query.filter(*queries).order_by(Tag.name).all()
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
tags_blueprint.add_url_rule(
    '/all',
    view_func=all_view,
    methods=['GET']
)
