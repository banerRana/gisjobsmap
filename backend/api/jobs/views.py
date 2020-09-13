import json
import os
from datetime import datetime, timedelta

from api import db
from api.auth.util import authenticate, user_detail
from api.categories.models import Category
from api.geonames.models import WorldBorders, Geoname
from api.tags.models import Tag
from api.utils import get_center_from_bounding_box
from flask import Blueprint, jsonify, request, make_response
from flask.views import MethodView
from sqlalchemy import func, or_, and_

from .models import Job

jobs_blueprint = Blueprint('jobs', __name__)

API_LIMIT = os.getenv('API_RESPONSE_LIMIT')


class CountApi(MethodView):
    """Get Job counts by country"""

    def get(self):
        try:
            result = db.session.query(Job.country_code, func.count(Job.country_code)). \
                filter(Job.is_active == True, or_(Job.invalid_geom == False, Job.is_remote == True),
                       or_(datetime.now() <= Job.expire_date, Job.expire_date == None)). \
                group_by(Job.country_code). \
                order_by(func.count(Job.country_code).desc()).limit(10)
            response_object = {
                'success': True,
                'data': [r for r in result],
            }
            return make_response(jsonify(response_object)), 200
        except Exception as e:
            response_object = {
                'success': False,
                'message': 'Error. {}'.format(str(e))
            }
            return make_response(jsonify(response_object)), 500


class AddAPI(MethodView):
    """
    Job Insert Resource
    """

    def post(self, user_id):
        post_data = request.get_json()
        try:
            user = user_detail(user_id)
            if not user:
                response_object = {
                    'success': False,
                    'message': 'You need to be registered to post a job.',
                }
                return make_response(jsonify(response_object)), 401
            categories = post_data.get('categories'),
            tags = post_data.get('tags'),
            job_vals = dict(
                indeed_key=post_data.get('indeedKey'),
                user_id=user_id,
                title=post_data.get('title'),
                logo=post_data.get('logo'),
                company=post_data.get('company'),
                url=post_data.get('url'),

                contact_name=post_data.get('contactName'),
                contact_phone=post_data.get('contactPhone'),
                contact_email=post_data.get('contactEmail'),

                description=post_data.get('description'),
                compensation=post_data.get('compensation'),
                career_level=post_data.get('careerLevel'),
                travel_percentage=post_data.get('travelPercentage'),
                security_clearance_req=post_data.get('securityClearanceReq'),
                security_type=post_data.get('securityType'),

                city=post_data.get('city'),
                state=post_data.get('state'),
                country_code=post_data.get('countryCode'),
                formatted_location=post_data.get('formattedLocation'),

                lat=post_data.get('lat', 0),
                lon=post_data.get('lon', 0),
                is_remote=post_data.get('isRemote'),
                indeed_search_term=post_data.get('searchTerm'),
                data_source=post_data.get('dataSource'),
                publish_date=post_data.get('publishDate')
            )
            if categories:
                job_vals['categories'] = [Category.get_or_create(name=c) for c in categories[0]]
            if tags:
                job_vals['tags'] = [Tag.get_or_create(name=t) for t in tags[0]]
            # insert the job
            new_job = Job(**job_vals)
            db.session.add(new_job)
            db.session.commit()
            response_object = {
                'success': True,
                'message': 'Successfully posted job.',
                'id': new_job.link
            }
            return make_response(jsonify(response_object)), 200
        except Exception as e:
            response_object = {
                'success': False,
                'message': 'Error. {}'.format(str(e))
            }
            return make_response(jsonify(response_object)), 500


class UpdateAPI(MethodView):
    """
    Job Update Resource
    """

    def post(self, user_id):
        post_data = request.get_json()
        try:
            user = user_detail(user_id)
            job_id = post_data.get('id')
            job = Job.query.filter_by(id=job_id).first()
            if job:
                if (user_id != job.user_id and job.data_source == 'gjm') or not user.admin:
                    response_object = {
                        'success': False,
                        'message': 'User does not own this job or is not an admin.'
                    }
                    return make_response(jsonify(response_object)), 401
                job.indeed_key = post_data.get('indeedKey')
                job.title = post_data.get('title')
                job.logo = post_data.get('logo')
                job.logo = post_data.get('logo')
                job.company = post_data.get('company')
                job.url = post_data.get('url')
                job.contact_name = post_data.get('contactName')
                job.contact_phone = post_data.get('contactPhone')
                job.contact_email = post_data.get('contactEmail')
                job.description = post_data.get('description')
                job.compensation = post_data.get('compensation')
                job.career_level = post_data.get('careerLevel')
                job.travel_percentage = post_data.get('travelPercentage')
                job.security_clearance_req = post_data.get('securityClearanceReq')
                job.security_type = post_data.get('securityType')
                job.city = post_data.get('city')
                job.state = post_data.get('state')
                job.country_code = post_data.get('countryCode')
                job.formatted_location = post_data.get('formattedLocation')
                job.lat = post_data.get('lat')
                job.lon = post_data.get('lon')
                job.is_remote = post_data.get('remote')
                job.data_source = 'gjm'
                job.edit_date = datetime.utcnow()
                categories = post_data.get('categories', [])
                tags = post_data.get('tags', [])
                if len(tags):
                    job.tags.clear()
                    for t in tags:
                        job.tags.append(Tag.get_or_create(name=t))
                if len(categories):
                    job.categories.clear()
                    for c in categories:
                        job.categories.append(Category.get_or_create(name=c))

                db.session.commit()
                Job.on_update(id=job_id)
                response_object = {
                    'success': True,
                    'message': 'Successfully updated job.',
                    'id': job.link
                }
                return make_response(jsonify(response_object)), 200
            else:
                response_object = {
                    'success': False,
                    'message': 'Job doesnt exist or no ID provided'
                }
                return make_response(jsonify(response_object)), 400
        except Exception as e:
            print("ERROR", e)
            response_object = {
                'success': False,
                'message': 'Error: {}'.format(e)
            }
            return make_response(jsonify(response_object)), 500


class AllAPI(MethodView):
    """
    All Jobs Resource
    """

    def get(self):
        get_data = request.args
        try:
            search_term = get_data.get('q')
            source = get_data.get('source', type=str)
            employer = get_data.get('organization')
            since = get_data.get('date')
            # remote = get_data.get('remote', default='true')
            # remote= json.loads(remote)
            map_only = get_data.get('maponly', default='false')
            map_only = json.loads(map_only)
            categories = get_data.get('categories', type=str)
            tags = get_data.get('tags', type=str)
            box = get_data.get('box', type=str)
            country = get_data.get('country', type=str)
            reverse_geocoded = {}
            queries = [Job.is_active == True,
                       or_(Job.is_remote != bool(map_only), Job.invalid_geom == False),
                       or_(datetime.now() <= Job.expire_date, Job.expire_date == None)]

            if tags:
                tags = tags.split(',')
                for tag in tags:
                    queries.append(Job.tags.any(Tag.name == tag))
            if categories:
                categories = categories.split(',')
                for c in categories:
                    queries.append(Job.categories.any(Category.name == c))
            if search_term:
                queries.append(Job.description.ilike('%{}%'.format(search_term)))
            if source:
                queries.append(Job.source == source)
            if employer:
                queries.append(Job.company.ilike('%{}%'.format(employer)))
            if since:
                days = datetime.today() - timedelta(days=int(since))
                queries.append(Job.publish_date > days)
            if country:
                queries.append(Job.country_code == country.lower())
            if box:
                countries_in_box = WorldBorders.countries_from_bounding_box(box=box)
                if len(countries_in_box) == 1:
                    map_center_point = get_center_from_bounding_box(box)
                    country = countries_in_box[0].lower()
                    rg = Geoname.reverse_geocode(lat=map_center_point[1],
                                                 lon=map_center_point[0],
                                                 min_population=10000,
                                                 country_code=country)

                    if len(rg):
                        reverse_geocoded = rg[0]

                else:
                    queries.append(Job.country_code.in_(countries_in_box))

                if map_only:
                    queries.append(Job.the_geom.intersects(func.ST_MakeEnvelope(*box.split(","))))
                else:
                    queries.append(or_(Job.the_geom.intersects(func.ST_MakeEnvelope(*box.split(","))),
                                       and_(Job.is_remote == True, Job.country_code.in_(countries_in_box))))
            jobs = Job.query.filter(*queries).order_by(Job.publish_date.desc()).limit(API_LIMIT)
            return make_response(
                jsonify({"success": True,
                         "data": [i.serialize_preview for i in jobs],
                         "near": reverse_geocoded,
                         "country": {'iso2': country if country else None,
                                     'name': WorldBorders.get_name_from_iso2(country) if country else None,
                                     'geom': json.loads(WorldBorders.get_country_geometry(country)) if country else {}
                                     }
                         })), 200
        except Exception as e:
            print('view error', e)
            response_object = {
                "success": False,
                'message': str(e)
            }
            return make_response(jsonify(response_object)), 500


class DetailAPI(MethodView):
    """
    Job Detail Resource
    """

    def get(self):
        get_data = request.args
        try:
            slug = get_data.get('slug')
            job_id = get_data.get('id')
            if slug:
                job = Job.query_from_slug(slug=slug)
                if job:
                    return make_response(jsonify(success=True, data=job.serialize_job)), 200
            elif job_id:
                job = Job.query.filter_by(id=job_id).first()
                if job:
                    return make_response(jsonify(success=True, data=job.serialize_job)), 200
            response_object = {
                'success': False,
                'message': 'Job doesnt exist or no slug/id provided'
            }
            return make_response(jsonify(response_object)), 400
        except Exception as e:
            print("error", e)
            response_object = {
                'success': False,
                'message': str(e)
            }
            return make_response(jsonify(response_object)), 500


class SetInactiveAPI(MethodView):
    """
    Sets a list of jobs inactive or active by `indeed_key` and 'task'
    """

    def post(self, user_id):
        post_data = request.get_json()
        try:
            user = user_detail(user_id)
            indeed_keys = post_data.get('keys')
            set_task = post_data.get('task')  # active or inactive
            if not indeed_keys:
                response_object = {
                    'success': False,
                    'message': "No indeed keys provided."
                }
                return make_response(jsonify(response_object)), 500
            if not user.admin:
                response_object = {
                    'success': False,
                    'message': "This api is restricted to administrators."
                }
                return make_response(jsonify(response_object)), 401
            if set_task.lower() == 'inactive':
                db.session.query(Job).filter(Job.indeed_key.in_(indeed_keys), Job.data_source == 'indeed').update(
                    {"is_active": False},
                    synchronize_session='fetch')
                db.session.commit()
                response_object = {
                    'success': True,
                    'message': 'set job(s) {}'.format(set_task)
                }
                return make_response(jsonify(response_object)), 200
            if set_task.lower() == 'active':
                db.session.query(Job).filter(Job.indeed_key.in_(indeed_keys), Job.data_source == 'indeed').update(
                    {"is_active": True},
                    synchronize_session='fetch')
                db.session.commit()
                response_object = {
                    'success': True,
                    'message': 'set job(s) {}'.format(set_task)
                }
                return make_response(jsonify(response_object)), 200
            response_object = {
                'success': False,
                'message': 'no update performed.'
            }
            return make_response(jsonify(response_object)), 200
        except Exception as e:
            response_object = {
                'success': False,
                'message': str(e)
            }
            return make_response(jsonify(response_object)), 500


class ValidKeysAPI(MethodView):
    """
    Returns a list of valid indeed job keys
    """

    def get(self):
        try:
            get_data = request.get_json()
            iso2 = get_data.get('iso2')
            if iso2:
                valid_active = db.session.query(Job.indeed_key).filter(
                    Job.data_source == 'indeed', Job.country_code == iso2.lower(), Job.is_active == True).all()
                valid_inactive = db.session.query(Job.indeed_key).filter(
                    Job.data_source == 'indeed', Job.country_code == iso2.lower(), Job.is_active == False).all()
                return make_response(
                    jsonify({"success": True,
                             "inactive": [v[0] for v in valid_inactive],
                             "active": [v[0] for v in valid_active]})), 200
            else:
                response_object = {
                    'success': False,
                    'message': 'Must supply an `iso2` parameter'
                }
                return make_response(jsonify(response_object)), 500
        except Exception as e:
            response_object = {
                'success': True,
                'message': str(e)
            }
            return make_response(jsonify(response_object)), 500


# define the API resources
count_view = CountApi.as_view('count_api')
add_view = AddAPI.as_view('add_api')
update_view = UpdateAPI.as_view('update_api')
all_view = AllAPI.as_view('all_api')
detail_view = DetailAPI.as_view('detail_api')
set_inactive_view = SetInactiveAPI.as_view('inactive_api')
valid_Keys_view = ValidKeysAPI.as_view('valid_api')

# add Rules for API Endpoints
jobs_blueprint.add_url_rule(
    '/counts',
    view_func=count_view,
    methods=['GET']
)
jobs_blueprint.add_url_rule(
    '/add',
    view_func=authenticate(add_view),
    methods=['POST']
)
jobs_blueprint.add_url_rule(
    '/update',
    view_func=authenticate(update_view),
    methods=['POST']
)
jobs_blueprint.add_url_rule(
    '/all',
    view_func=all_view,
    methods=['GET']
)
jobs_blueprint.add_url_rule(
    '/detail',
    view_func=detail_view,
    methods=['GET']
)
jobs_blueprint.add_url_rule(
    '/inactive',
    view_func=authenticate(set_inactive_view),
    methods=['POST']
)
jobs_blueprint.add_url_rule(
    '/valid',
    view_func=valid_Keys_view,
    methods=['GET']
)
