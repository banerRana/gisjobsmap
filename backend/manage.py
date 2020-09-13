import os
from termcolor import colored
import coverage
import unittest
import datetime
from flask.cli import FlaskGroup
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles
import csv

from api import create_app, db
from api.jobs.models import Job
from api.organizations.models import Organization
from api.auth.models import User
from api.tags.models import Tag
from api.categories.models import Category
from api.scraper.models import Invalid
from api.geonames.models import WorldBorders

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(dir_path, "data")


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


COV = coverage.coverage(
    branch=True,
    include='api/*',
    omit=[
        'tests/*',
        'config.py',
        'api/*/__init__.py'
    ]
)
COV.start()

app = create_app()
migrate = Migrate(app, db)
cli = FlaskGroup(create_app=create_app)

# migrations
cli.add_command('db', MigrateCommand)


@cli.command('test')
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command('cov')
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


def load_users():
    print("creating users...")

    admin_user = User(email=os.getenv('ADMIN_USER'),
                      password=os.getenv('ACCOUNT_PASSWORD'),
                      admin=True,
                      confirmed=True,
                      confirmed_on=datetime.datetime.utcnow())
    db.session.add(admin_user)

    scraper = User(email=os.getenv('SCRAPE_USER'),
                   password=os.getenv('ACCOUNT_PASSWORD'),
                   admin=True,
                   confirmed=True,
                   confirmed_on=datetime.datetime.utcnow())
    db.session.add(scraper)
    db.session.commit()

    anon = User(email='anonymous@anonymous.com',
                password=os.getenv('ACCOUNT_PASSWORD'),
                admin=False,
                confirmed=True,
                confirmed_on=datetime.datetime.utcnow())

    db.session.add(anon)
    db.session.commit()

    print(colored('Created Admin and Scraper users', 'green'))


@cli.command('init_data')
def init_data():
    db.drop_all(bind=None)
    db.create_all(bind=None)
    db.session.commit()
    load_users()
    load_tags()
    load_categories()


@cli.command('init_geo')
def init_geo():
    db.drop_all(bind='geonames')
    db.create_all(bind='geonames')
    db.session.commit()
    load_world_borders()
    load_admin1_codes()
    load_admin2_codes()
    load_geonames()


@cli.command('init_all')
def init_all():
    recreate_db()
    # init_users()
    init_data()


def load_invalid_keys():
    print('loading invalid job keys...')
    try:
        file_name = os.path.join('data', "invalid.copy")
        with open(file_name, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            # data = Load_Data(file_name)
            for row in reader:
                if row[0]:
                    str2date = datetime.datetime.strptime(row[1].split(" ")[0], '%Y-%m-%d')
                    record = Invalid(
                        key=row[0],
                        scrape_date=str2date
                    )
                    db.session.add(record)  # Add all the records
            db.session.commit()  # Attempt to commit all the records
    except Exception as e:
        db.session.rollback()  # Rollback the changes on error
        print(colored('Invalid Keys: {}'.format(str(e)), 'red'))
    finally:
        db.session.close()  # Close the connection
        print(colored('Loaded Invalid Keys', 'green'))


def load_job_data():
    print('loading job data...')
    try:
        file_name = os.path.join('data', "job.copy")
        with open(file_name, 'r', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                if row[0]:
                    try:
                        str2date = datetime.datetime.strptime(row[10].split(" ")[0], '%Y-%m-%d')
                        record = Job(
                            indeed_key=row[0],
                            data_source='indeed',
                            title=row[1],
                            company=row[2],
                            city=row[3],
                            state=row[4],
                            country_code=row[5],
                            formatted_location=row[6],
                            url=row[7],
                            indeed_search_term=row[8],
                            description=row[9],
                            publish_date=str2date,
                            is_active=False,
                            lon=row[12],
                            lat=row[13],
                            user_id=1)
                        db.session.add(record)  # Add the records
                    except Exception as e:
                        print(e)
                        continue
                    db.session.commit()  # Attempt to commit all the records
    except Exception as e:
        db.session.rollback()  # Rollback the changes on error
        print(colored('Job data: {}'.format(str(e)), 'red'))
    finally:
        db.session.close()  # Close the connection
        print(colored('Loaded job data', 'green'))


def load_organization_data():
    print('loading organization data...')
    try:
        file_name = os.path.join('data', "organization.copy")
        with open(file_name, 'r', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                if row[0]:
                    try:
                        record = Organization(
                            name=row[0],
                            city=row[1],
                            state=row[2],
                            formatted_location=row[3],
                            country_code=row[4],
                            lon=row[5],
                            lat=row[6],
                            user_id=1)
                        db.session.add(record)  # Add the records
                    except Exception as e:
                        print(e)
                        continue
                    db.session.commit()  # Attempt to commit all the records
    except Exception as e:
        db.session.rollback()  # Rollback the changes on error
        print(colored('Organization data: {}'.format(str(e)), 'red'))
    finally:
        db.session.close()  # Close the connection
        print(colored('Loaded Organization data', 'green'))


def load_world_borders():
    import zipfile
    world_borders_csv = 'data/world-borders.csv'
    world_borders_zip = 'data/world-borders.zip'
    if not os.path.exists(world_borders_csv):
        with zipfile.ZipFile(world_borders_zip, 'r') as zip_ref:
            zip_ref.extractall('data')
    try:
        with open(world_borders_csv, 'r', encoding="utf8") as csvfile:
            csv.field_size_limit(100000000)
            data_reader = csv.reader(csvfile, delimiter=',')
            next(data_reader, None)  # skip the headers
            for row in data_reader:
                new_country = WorldBorders(
                    geom=row[0],
                    fips=row[1],
                    iso2=row[2],
                    iso3=row[3],
                    un=row[4],
                    name=row[5],
                    area=row[6],
                    pop2005=row[7],
                    region=row[8],
                    subregion=row[9],
                    lon=row[10],
                    lat=row[11]
                )
                db.session.add(new_country)
                db.session.commit()
        print(colored('Loaded WorldBorders', 'green'))
    except Exception as e:
        print('WORLD BORDERS ERROR: ', e)


def load_tags():
    print("loading users...")
    try:
        with open(os.path.join('data', "tags.csv", ), encoding="utf8") as csvfile:
            data_reader = csv.reader(csvfile, delimiter=',')
            next(data_reader, None)  # skip the headers
            for row in data_reader:
                new_tag = Tag(
                    valid=True,
                    name=row[0],
                    gis=True if row[1] == '1' else False
                )
                db.session.add(new_tag)
                db.session.commit()
        print(colored('Loaded tags', 'green'))
    except Exception as e:
        print(colored(e, 'red'))


def load_categories():
    print("loading categories...")
    try:
        with open(os.path.join('data', "categories.csv"), encoding="utf8") as csvfile:
            data_reader = csv.reader(csvfile, delimiter=',')
            next(data_reader, None)  # skip the headers
            for row in data_reader:
                new_category = Category(
                    valid=True,
                    name=row[0],
                    searches=row[1].strip())
                db.session.add(new_category)
                db.session.commit()
        print(colored('Loaded categories', 'green'))
    except Exception as e:
        print(colored(e, 'red'))


def load_admin1_codes(file=None, cnx=None):
    """
    Load admin 1 codes
    :param file: input file for unit testing
    :param cnx: database connection for unit testing
    :return: None
    """
    if not file:
        file = download_and_extract('admin1CodesASCII.txt')
    with open(file, 'r', encoding='utf8') as f:
        conn = db.create_engine(cnx if cnx else app.config['SQLALCHEMY_BINDS']['geonames'], {}).raw_connection()
        cursor = conn.cursor()
        cmd = '''    
        COPY admin1code(code, name, name_ascii, geonameid) FROM STDIN WITH delimiter E'\t' null as ''
        '''
        cursor.copy_expert(cmd, f)
        cursor.execute(
            "UPDATE admin1code SET country_code = SPLIT_PART(code, '.', 1);"
            "UPDATE admin1code SET admin1 = SPLIT_PART(code, '.', 2);"
            "")
        conn.commit()
    if not cnx:
        print('populated the admin codes table.')


def load_admin2_codes(file=None, cnx=None):
    """
    Load admin 2 codes
    :param file: input file for unit testing
    :param cnx: database connection for unit testing
    :return: None
    """
    if not file:
        file = download_and_extract('admin2Codes.txt')
    with open(file, 'r', encoding='utf8') as f:
        conn = db.create_engine(cnx if cnx else app.config['SQLALCHEMY_BINDS']['geonames'], {}).raw_connection()
        cursor = conn.cursor()
        cmd = '''    
        COPY admin2code(code, name, name_ascii, geonameid) FROM STDIN WITH delimiter E'\t' null as ''
        '''
        cursor.copy_expert(cmd, f)
        cursor.execute(
            "UPDATE admin2code SET country_code = SPLIT_PART(code, '.', 1);"
            "UPDATE admin2code SET admin1 = SPLIT_PART(code, '.', 2);"
            "UPDATE admin2code SET admin2 = SPLIT_PART(code, '.', 3);"
            "")
        conn.commit()
    if not cnx:
        print('populated the admin 2 codes table.')


def load_geonames(file=None, cnx=None):
    """
    Load geonames data
    :param file: input file for unit testing
    :param cnx: database connection for unit testing
    :return: None
    """
    if not file:
        file = download_and_extract(os.getenv('GEONAMES_DATA') + ".zip")
        print("importing geonames data...")
    with open(file, 'rb') as f:
        conn = db.create_engine(cnx if cnx else app.config['SQLALCHEMY_BINDS']['geonames'], {}).raw_connection()
        cursor = conn.cursor()
        cmd = '''    
        COPY geoname(geonameid, name, asciiname, alternatenames, latitude, longitude, feature_class, feature_code, 
        country_code, cc2, admin1, admin2, admin3, admin4, population, elevation, gtopo30, timezone, moddate) 
        FROM STDIN WITH delimiter E'\t' null as ''
        '''
        cursor.copy_expert(cmd, f)
        cursor.execute(
            "UPDATE geoname SET the_geom = ST_PointFromText('POINT(' || longitude || ' ' || latitude || ')', 4326);"
        )
        # cursor.execute(
        #     "UPDATE geoname SET the_geom = ST_PointFromText('POINT(' || longitude || ' ' || latitude || ')', 4326);"
        # )
        conn.commit()
    if not cnx:
        print('populated the geonames table.')


def download_and_extract(file_name):
    """
    Downloads from geoname dump and returns the local .txt file location
    :param file_name: input filename to download (.txt or .zip)
    :return: full pathname of downloaded/extracted file.
    """
    from tqdm import tqdm
    import requests
    import zipfile
    print('downloading {}...'.format(file_name))
    url = "http://download.geonames.org/export/dump/{}".format(file_name)
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    dest_path = os.path.join(data_path, file_name)
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        total_size = int(r.headers.get('content-length', 0))
        block_size = 1024  # 1 kb
        t = tqdm(total=total_size, unit='iB', unit_scale=True)
        with open(dest_path, "wb") as handle:
            for data in tqdm(r.iter_content(block_size)):
                t.update(len(data))
                handle.write(data)
        t.close()
        if total_size != 0 and t.n != total_size:
            raise Exception("Error downloading {}".format(file_name))
        if ".zip" in file_name:
            with zipfile.ZipFile(dest_path, 'r') as zip_ref:
                zip_ref.extractall(data_path)
            dest_path = os.path.join(data_path, file_name.split(".zip")[0] + ".txt")
        return dest_path
    else:
        raise Exception('Error reaching Geonames server. {} {}.'.format(r.status_code, r.reason))


if __name__ == '__main__':
    cli()
