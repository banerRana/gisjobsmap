from flask_admin.contrib.geoa import ModelView
from flask_admin.model import typefmt
from flask import url_for, redirect, request
import flask_admin as admin
import flask_login as login
from flask_admin import helpers, expose
from datetime import date

from .admin_form import LoginForm


def date_format(view, value):
    return value.strftime('%Y-%m-%d')


MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({
    type(None): typefmt.null_formatter,
    date: date_format
})


# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            form.validate_login()
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


class CustomModelView(ModelView):
    create_modal = True
    edit_modal = True
    can_export = True
    page_size = 50

    def is_accessible(self):
        return login.current_user.is_authenticated


class JobModelView(ModelView):
    column_type_formatters = MY_DEFAULT_FORMATTERS
    column_searchable_list = ('title', 'company')
    column_filters = (
        'title', 'company', 'publish_date', 'expire_date', 'is_active', 'formatted_location', 'country_code',
        'data_source', 'invalid_geom', 'is_remote')
    column_list = (
    'title', 'company', 'publish_date', 'expire_date', 'is_active', 'data_source', 'formatted_location', 'country_code')
    column_default_sort = [('data_source', False), ('is_active', True), ('publish_date', True), ('country_code', False)]
    form_columns = (
        'is_active', 'indeed_key', 'data_source', 'title', 'company', 'tags', 'categories', 'compensation', 'slug',
        'url', 'publish_date', 'expire_date',
        'is_remote', 'city', 'state', 'formatted_location', 'country_code', 'description', 'invalid_geom', 'the_geom')
    form_widget_args = {
        'description': {
            'rows': 20,
            'style': 'color: black'
        },
    }

    create_modal = True
    edit_modal = True
    can_export = True
    can_delete = False
    page_size = 50

    def is_accessible(self):
        return login.current_user.is_authenticated


class CategoryModelView(ModelView):
    column_type_formatters = MY_DEFAULT_FORMATTERS
    column_searchable_list = ('name', 'valid', 'searches')
    column_filters = ('name', 'valid', 'searches')
    column_list = ('name', 'valid', 'searches')
    column_default_sort = [('name', True), ('valid', False), ('searches', False)]
    form_columns = ('name', 'valid', 'searches')

    create_modal = True
    edit_modal = True
    can_export = True
    can_delete = False
    page_size = 50

    def is_accessible(self):
        return login.current_user.is_authenticated


class TagModelView(ModelView):
    column_type_formatters = MY_DEFAULT_FORMATTERS
    column_searchable_list = ('name', 'valid', 'gis')
    column_filters = ('name', 'valid', 'gis')
    column_list = ('name', 'valid', 'gis')
    column_default_sort = [('name', True), ('valid', False), ('gis', False)]
    form_columns = ('name', 'valid', 'gis')

    create_modal = True
    edit_modal = True
    can_export = True
    can_delete = False
    page_size = 50

    def is_accessible(self):
        return login.current_user.is_authenticated