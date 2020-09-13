from flask import request, jsonify
from api import db
from datetime import datetime, timedelta
import json
from sqlalchemy import func
from flask import Blueprint

from api.categories.models import Category
from api.tags.models import Tag
from .models import Resume


resumes_blueprint = Blueprint('resumes', __name__)


@resumes_blueprint.route("/detail", methods=["GET"])
def job_detail():
    id = request.args.get('jobid')
    if id:
        result = db.session.query(Resume).filter(Resume.id == id).first()
        if result:
            result.clicks = Resume.clicks + 1
            db.session.commit()
            return jsonify(results=result.serialize_job)
    return jsonify(results={})


@resumes_blueprint.route("/add", methods=["POST"])
def add_job():
    data = request.get_json()
    try:
        new_job = Resume(indeed_key=data.get('indeed_key', None),
                         user_id=1,
                         company=data.get('company', None),
                         snippet=data.get('snippet', None),
                         city=data.get('city', None),
                         state=data.get('state', None),
                         country_code=data.get('country_code', None),
                         formattedlocation=data.get('formatted_location', None),
                         publish_date=data.get('date4db', None),
                         url=data.get('url', None),
                         category=data.get('category', None),
                         description=data.get('description', None),
                         the_geom='SRID=4326;POINT({} {})'.format(float(data.get('lng', 0)),
                                                                  float(data.get('lat', 0)))
                         )
        db.session.add(new_job)
        db.session.commit()
        return 'success', 200
    except Exception as e:
        return str(e), 500


@resumes_blueprint.route("/all", methods=["GET"])
def all_jobs():
    search_term = request.args.get('search')
    source = request.args.get('source')
    employer = request.args.get('organization')
    since = request.args.get('since')
    is_remote = request.args.get('remote')
    tags = request.args.get('tags')
    category = request.args.get('category')
    box = request.args.get('box')
    country = request.args.get('iso2')

    queries = []

    queries.append(Resume.is_active)

    if country:
        queries.append(Resume.country_code == country.lower())
    else:
        return "must provide iso2 country code", 204

    if tags:
        tags = json.loads(tags)
        for tag in tags:
            queries.append(Resume.tags.any(Tag.name == tag))

    if category:
        queries.append(Resume.categories.any(Category.name == category))

    if search_term:
        queries.append(Resume.description.ilike('%{}%'.format(search_term)))

    if source:
        queries.append(Resume.source == source)

    if employer:
        queries.append(Resume.company.ilike('%{}%'.format(employer)))

    if since:
        days = datetime.now() - timedelta(days=int(since))
        queries.append(Resume.publish_date > days)

    if is_remote:
        queries.append(Resume.is_remote == is_remote)

    if box:
        queries.append(Resume.the_geom.intersects(func.ST_MakeEnvelope(*box.split(","))))

    resumes = Resume.query.filter(*queries).all()
    return jsonify({"type": "FeatureCollection", "features": [i.serialize_preview for i in resumes]})
