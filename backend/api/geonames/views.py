from api import geoip_data
from api.geonames.models import Geoname, WorldBorders
from flask import Blueprint, jsonify, request, make_response
from flask.views import MethodView

geonames_blueprint = Blueprint('geonames', __name__)


class GeoIPAPI(MethodView):
    """
    Get user location by IP address for map orientation
    """

    def get(self):
        try:
            ip = request.access_route[0]
            if ip in ['127.0.0.1', 'localhost', '0.0.0.0']:  # for testing
                response = geoip_data.city('96.225.93.125')
            else:
                response = geoip_data.city(ip)
            iso2 = response.country.iso_code
            city = response.city.name
            country_name = response.country.name
            lat = response.location.latitude
            lon = response.location.longitude

            responseObject = {
                'success': True,
                'data': {'iso2': iso2.lower(),
                         'geonameId': response.city.geoname_id,
                         'country': country_name,
                         'city': city,
                         'coordinates': [lat, lon]}
            }
            return make_response(jsonify(responseObject)), 200

        except Exception as e:
            responseObject = {
                'success': False,
                'message': str(e)
            }
            return make_response(jsonify(responseObject)), 400


class WithinCountryAPI(MethodView):
    """
    Check if point falls within a country Resource
    """

    def get(self):
        get_data = request.args
        try:
            iso2 = get_data.get('iso2')
            lat = get_data.get('lat')
            lon = get_data.get('lon')
            result = WorldBorders.is_within(iso2=iso2, lat=lat, lon=lon)

            return make_response(
                jsonify({'success': True,
                         'data': result
                         })), 200

        except Exception as e:
            responseObject = {
                'success': False,
                'message': str(e)
            }
            return make_response(jsonify(responseObject)), 500


class ReverseGeocodeAPI(MethodView):
    """
    Get Nearest City based on input lat/lon Resource
    """

    def get(self):
        get_data = request.args
        try:
            lat = get_data.get('lat')
            lon = get_data.get('lon')
            accuracy = get_data.get('accuracy', .01)  # set default accuracy here
            feature_code = get_data.get('featureCode')
            feature_class = get_data.get('featureClass')
            if lat and lon:
                result = Geoname.reverse_geocode(lat=lat,
                                                 lon=lon,
                                                 accuracy=accuracy,
                                                 feature_code=feature_code,
                                                 feature_class=feature_class)
                return make_response(
                    jsonify({'success': True,
                             "data": result
                             })), 200
            else:
                return make_response(
                    jsonify({'success': False,
                             'message': 'Must supply both `lat` and `lon` parameters.'
                             })), 400
        except Exception as e:
            response_object = {
                'success': False,
                'message': str(e)
            }
            return make_response(jsonify(response_object)), 500


class GeocodeAPI(MethodView):
    """
    Get Nearest City based on input lat/lon Resource
    """

    def get(self):
        get_data = request.args
        try:
            iso2 = get_data.get('iso2')
            text = get_data.get('text')
            name = get_data.get('name')
            admin1 = get_data.get('admin1')
            admin2 = get_data.get('admin2')
            feature_code = get_data.get('featureCode')
            feature_class = get_data.get('featureClass')
            result = Geoname.geocode(text=text,
                                     iso2=iso2,
                                     name=name,
                                     admin1=admin1,
                                     admin2=admin2,
                                     feature_code=feature_code,
                                     feature_class=feature_class
                                     )
            return make_response(
                jsonify({'success': True,
                         'data': result
                         })), 200
        except Exception as e:
            response_object = {
                'success': False,
                'message': str(e)
            }
            return make_response(jsonify(response_object)), 500


geoip_view = GeoIPAPI.as_view('geoip_api')
within_country_view = WithinCountryAPI.as_view('within_country_api')
reverse_geocode_view = ReverseGeocodeAPI.as_view('reverse_geocode_api')
geocode_view = GeocodeAPI.as_view('geocode_api')

# add Rules for API Endpoints
geonames_blueprint.add_url_rule(
    '/geoip',
    view_func=geoip_view,
    methods=['GET']
)
geonames_blueprint.add_url_rule(
    '/within',
    view_func=within_country_view,
    methods=['GET']
)
geonames_blueprint.add_url_rule(
    '/reverse-geocode',
    view_func=reverse_geocode_view,
    methods=['GET']
)
geonames_blueprint.add_url_rule(
    '/geocode',
    view_func=geocode_view,
    methods=['GET']
)
