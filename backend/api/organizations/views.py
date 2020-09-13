from datetime import datetime

from api import db
from api.auth.util import authenticate, user_detail
from flask import Blueprint, jsonify, request, make_response
from flask.views import MethodView
from sqlalchemy import func

from .models import Organization

organizations_blueprint = Blueprint('organizations', __name__)

mapper = dict(name='name',
              headline='headline',
              year_founded='yearFounded',
              size='size',
              logo='logo',
              url='url',
              description='description',
              sector='sector',
              contact_name='contactName',
              contact_phone='contactPhone',
              contact_email='contactEmail',
              hires_remote='hiresRemote',
              is_distributed='isDistributed',
              street_address='streetAddress',
              city='city',
              state='state',
              postal_code='postalCode',
              country_code='countryCode',
              formatted_location='formattedLocation',
              lat='lat',
              lon='lon',
              edit_date=datetime.utcnow())


class AddAPI(MethodView):
    """
    Organization Add Resource
    """

    def post(self, user_id):
        post_data = request.get_json()
        try:
            user = user_detail(user_id)
            if not user:
                response_object = {
                    'success': False,
                    'message': 'You need to be registered to post an organization.',
                }
                return make_response(jsonify(response_object)), 401

            org = Organization(
                user_id=user_id,
                name=post_data.get('name', None),
                headline=post_data.get('headline', None),
                year_founded=post_data.get('yearFounded', None),
                size=post_data.get('size', None),
                logo=post_data.get('logo', None),
                url=post_data.get('url', None),
                description=post_data.get('description', None),
                sector=post_data.get('sector', None),
                contact_name=post_data.get('contactName', None),
                contact_phone=post_data.get('contactPhone', None),
                contact_email=post_data.get('contactEmail', None),
                hires_remote=post_data.get('hiresRemote', None),
                is_distributed=post_data.get('isDistributed', None),
                data_source=post_data.get('dataSource', None),
                street_address=post_data.get('streetAddress', None),
                city=post_data.get('city', None),
                state=post_data.get('state', None),
                postal_code=post_data.get('postalCode', None),
                country_code=post_data.get('countryCode', None),
                lat=post_data.get('lat', None),
                lon=post_data.get('lon', None),
            )
            # insert the org
            db.session.add(org)
            db.session.commit()
            response_object = {
                'success': True,
                'message': 'Successfully posted organization.',
                'id': org.id
            }
            return make_response(jsonify(response_object)), 200
        except Exception as e:
            print('error', e)
            response_object = {
                'success': False,
                'message': 'Error. {}'.format(e)
            }
            return make_response(jsonify(response_object)), 500


class UpdateAPI(MethodView):
    """
    Organization Update Resource
    """

    def post(self, user_id):
        post_data = request.get_json()
        try:
            user = user_detail(user_id)
            org_id = post_data.get('id')
            org = Organization.query.filter_by(id=org_id).first()
            if org:
                if user_id != org.user_id or not user.admin:
                    response_object = {
                        'success': False,
                        'message': 'User does not own organization or is not an admin.'
                    }
                    return make_response(jsonify(response_object)), 401
                # update the organization
                org_vals = dict(
                    user_id=user.id if user.admin else user.admin,
                    name=post_data.get('name'),
                    headline=post_data.get('headline'),
                    year_founded=post_data.get('size'),
                    size=post_data.get('size'),
                    logo=post_data.get('logo'),
                    url=post_data.get('url'),
                    description=post_data.get('description'),
                    sector=post_data.get('sector'),
                    contact_name=post_data.get('contactName'),
                    contact_phone=post_data.get('contactPhone'),
                    contact_email=post_data.get('contactEmail'),
                    hires_remote=post_data.get('hiresRemote'),
                    is_distributed=post_data.get('isDistributed'),
                    street_address=post_data.get('streetAddress'),
                    city=post_data.get('city'),
                    state=post_data.get('state'),
                    postal_code=post_data.get('postalCode'),
                    country_code=post_data.get('countryCode'),
                    formatted_location=post_data.get('formattedLocation'),
                    lat=post_data.get('lat'),
                    lon=post_data.get('lon'),
                    edit_date=datetime.utcnow()
                )
                org_id = db.session.query(Organization).filter_by(id=org_id).update(org_vals,
                                                                                    synchronize_session='fetch')
                Organization.on_update(id=org_id)
                db.session.commit()
                response_object = {
                    'success': True,
                    'message': 'Successfully updated organization.',
                    'id': org_id
                }
                return make_response(jsonify(response_object)), 200
            else:
                responseObject = {
                    'success': False,
                    'message': 'org doesnt exist or no ID provided'
                }
                return make_response(jsonify(responseObject)), 400
        except Exception as e:
            print('error', e)
            responseObject = {
                'success': False,
                'message': 'Error. {}'.format(e)
            }
            return make_response(jsonify(responseObject)), 500


class AllAPI(MethodView):
    """
    Organization - get all orgs Resource
    """

    def get(self):
        get_data = request.args
        try:
            queries = []

            if get_data:
                search_term = get_data.get('q')
                name = get_data.get('name')
                hires_remote = get_data.get('hiresRemote')
                box = get_data.get('box')
                country = get_data.get('country')
                sector = get_data.get('type')

                if country:
                    queries.append(Organization.country_code == country.lower())
                if sector:
                    queries.append(Organization.sector == sector)
                if search_term:
                    queries.append(Organization.description.ilike('%{}%'.format(search_term)))
                if hires_remote:
                    queries.append(Organization.hires_remote)
                if name:
                    queries.append(Organization.name.ilike('%{}%'.format(name)))
                if box:
                    queries.append(Organization.the_geom.intersects(func.ST_MakeEnvelope(*box.split(","))))
            orgs = Organization.query.filter(*queries).order_by(Organization.edit_date.desc()).limit(200)
            return make_response(
                jsonify({"success": True,
                         "data": {
                             "type": "FeatureCollection",
                             "features": [i.serialize_preview for i in orgs]
                         }
                         })), 200
        except Exception as e:
            responseObject = {
                'success': False,
                'message': str(e)
            }
            return make_response(jsonify(responseObject)), 501


class DetailAPI(MethodView):
    """
    Detail Resource
    """

    def get(self):
        get_data = request.get_json()
        try:
            slug = get_data.get('slug')
            org_id = get_data.get('id')
            if slug:
                org = Organization.query_from_slug(slug=slug)
                if org:
                    org.clicks = Organization.clicks + 1
                    db.session.commit()
                    return make_response(jsonify(success=True, data=org.serialize_org)), 200
            elif org_id:
                org = Organization.query.filter_by(id=org_id).first()
                if org:
                    org.clicks = Organization.clicks + 1
                    db.session.commit()
                    return make_response(jsonify(success=True, data=org.serialize_org)), 200
            responseObject = {
                'success': False,
                'message': 'Job doesnt exist or no ID provided'
            }
            return make_response(jsonify(responseObject)), 400

        except Exception as e:
            responseObject = {
                'success': False,
                'message': str(e)
            }
            return make_response(jsonify(responseObject)), 501


# define the API resources
add_view = AddAPI.as_view('add_api')
update_view = UpdateAPI.as_view('update_api')
all_view = AllAPI.as_view('all_api')
detail_view = DetailAPI.as_view('detail_api')

# add Rules for API Endpoints
organizations_blueprint.add_url_rule(
    '/add',
    view_func=authenticate(add_view),
    methods=['POST']
)
organizations_blueprint.add_url_rule(
    '/update',
    view_func=authenticate(update_view),
    methods=['POST']
)
organizations_blueprint.add_url_rule(
    '/all',
    view_func=all_view,
    methods=['GET']
)
organizations_blueprint.add_url_rule(
    '/detail',
    view_func=detail_view,
    methods=['GET']
)
