from wtforms import form, fields, validators
from api import bcrypt
from api.auth.models import User
from api import db

# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    email = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        if not user.admin:
            raise validators.ValidationError('Invalid Permissions')

        if not user.confirmed:
            raise validators.ValidationError('User Not Confirmed')

        # we're comparing the plaintext pw with the the hash from the db
        if not bcrypt.check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User).filter_by(email=self.email.data).first()
