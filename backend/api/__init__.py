import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_admin import Admin
import flask_login as login
from flask_mail import Mail, Message
import geoip2.database
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

logging.basicConfig(level=logging.ERROR, filename='flaskapp.log', filemode='w',
                    format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d, %H:%M:%S')

geoip_data = geoip2.database.Reader(os.path.join(basedir, '..', 'data', 'GeoLite2-City.mmdb'))


# instantiate the extensions
db = SQLAlchemy()
toolbar = DebugToolbarExtension()
cors = CORS()
migrate = Migrate()
bcrypt = Bcrypt()
mail = Mail()


def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    from api.admin.admin_view import MyAdminIndexView
    admin = Admin(app, name='GJM Admin',
                  index_view=MyAdminIndexView(),
                  base_template='master.html',
                  template_mode='bootstrap3')

    login_manager = login.LoginManager()

    # Initialize extensions
    mail.init_app(app)
    db.init_app(app)
    toolbar.init_app(app)
    cors.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Create user loader function for Admin
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

    # setup admin models
    from api.auth.models import User, BlacklistToken, Searches
    from api.jobs.models import Job, job_tags, job_categories
    from api.tags.models import Tag
    from api.categories.models import Category
    from api.admin.admin_view import CustomModelView, JobModelView, TagModelView, CategoryModelView
    from api.resumes.models import Resume
    from api.scraper.models import Invalid, Status
    from api.organizations.models import Organization

    admin.add_view(JobModelView(Job, db.session, category="Jobs"))
    admin.add_view(CustomModelView(Searches, db.session, category="Jobs"))
    admin.add_view(CustomModelView(Invalid, db.session, category="Scraper"))
    admin.add_view(CustomModelView(Status, db.session, category="Scraper"))
    admin.add_view(CustomModelView(Resume, db.session))
    admin.add_view(TagModelView(Tag, db.session))
    admin.add_view(CategoryModelView(Category, db.session))
    admin.add_view(CustomModelView(Organization, db.session, category="Organizations"))
    admin.add_view(CustomModelView(User, db.session, category="Users"))
    admin.add_view(CustomModelView(BlacklistToken, db.session, category="Users"))

    # register blueprints
    from api.jobs.views import jobs_blueprint
    app.register_blueprint(jobs_blueprint, url_prefix='/api/jobs')

    from api.scraper.views import scraper_blueprint
    app.register_blueprint(scraper_blueprint, url_prefix='/api/scraper')

    from api.organizations.views import organizations_blueprint
    app.register_blueprint(organizations_blueprint, url_prefix='/api/organizations')

    from api.resumes.views import resumes_blueprint
    app.register_blueprint(resumes_blueprint, url_prefix='/api/resumes')

    from api.geonames.views import geonames_blueprint
    app.register_blueprint(geonames_blueprint, url_prefix='/api/geonames')

    from api.categories.views import categories_blueprint
    app.register_blueprint(categories_blueprint, url_prefix='/api/categories')

    from api.tags.views import tags_blueprint
    app.register_blueprint(tags_blueprint, url_prefix='/api/tags')

    from api.auth.views import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
