from geodaisy import GeoObject
from shapely import wkb, wkt, geometry
import numpy


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


def get_centroid(box):
    str_poly = "POLYGON(({}))".format(box)
    print(str_poly)
    p = wkt.loads(str_poly)
    return p.centroid


def is_global_view(box):
    box = box.split(",")
    if len(box):
        if len(box) == 4:
            box = [float(b) for b in box]
            point_1 = geometry.Point(*box[:2])
            point_2 = geometry.Point(*box[-2:])
            dist = point_1.distance(point_2)
            if dist < 15:
                return False
            return True
    return True


def get_center_from_bounding_box(box):
    split_box = box.split(",")
    if len(split_box):
        if len(split_box) == 4:
            coords = tuple(float(i) for i in split_box)
            pair_1 = (coords[0], coords[2])
            pair_2 = (coords[1], coords[3])
            return numpy.average(pair_1), numpy.average(pair_2)
    return None


def dump_geo(geom):
    """
    builds the geojson geometry for web response.
    :param geom: POINT geometry
    :return: geojson geometry, else None
    """
    if geom is not None:
        p = wkb.loads(bytes(geom.data))
        return {'type': 'Point',
                'coordinates': [p.x, p.y]}
    return None


def dump_country_geo(geom):
    if geom is not None:
        data = wkb.loads(bytes(geom.data)).simplify(tolerance=.3, preserve_topology=False).buffer(.2).simplify(tolerance=.1, preserve_topology=False)
        return GeoObject(data).geojson()
    return None


def dump_results(results):
    return [{
        'type': 'Feature',
        'properties': {
            'id': r.id,
            'name': r.name,
            'admin1': r.admin1,
            'admin2': r.admin2,
            'iso2': r.country_code,
            'featureClass': r.feature_class,
            'featureCode': r.feature_code,
            'population': r.population,
            'elevation': r.elevation,
            'gtopo30': r.gtopo30,
            'timezone': r.timezone,
            'moddate': r.moddate,
        },
        'geometry': dump_geo(r.the_geom),
    } for r in results]


def get_slug(id, slug):
    return "{}-{}".format(id, slug)
