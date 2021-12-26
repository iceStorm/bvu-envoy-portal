from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms.fields import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp, ValidationError

import re
from src.main.modules.user.user_model import User
from src.main.modules.auth.auth_service import AuthService
from src.main.base.helpers.validators import *


def IsEmailExists(form, field):
    """
    Checking if the email that client entered is have already exist.
    """
    if not AuthService.is_user_already_exists(field.data):
        raise ValidationError(message='The email is not registered')


class LoginForm(FlaskForm):
    email = EmailField(
        label='Email',
        description={
            'icon': {
                'origin': 'icons/outline/finger-print-outline.svg',
            },
        },
        render_kw={
            'autocomplete': 'email',
        },
        validators=[
            InputRequired(),
            EmailValidator,
            IsEmailExists,
        ]
    )

    password = PasswordField(
        label='Password',
        render_kw={'autocomplete': 'current-password'},
        description={
            'icon': {
                'origin': 'icons/outline/lock-closed-outline.svg',
                'alternate': 'icons/outline/lock-open-outline.svg',
            },
        },
        validators=[
            InputRequired(message='Please fill out this field'),
            PasswordValidator,
        ]
    )

    remember = BooleanField(
        label='Remember',
    )

    # overriding the validate function
    def validate(self):
        # first, validate the above requirements by: passing this instance to the FlaskForm.validate()
        if not FlaskForm.validate(self):
            return False

        # checking if the provided password is not True (with the one in the database)
        # the user instance below is always exists because the form's email validation did check.
        user = User.query.get(self.email.data)

        if not user.check_password(self.password.data):
            self.password.errors.append('The password you just provided was wrong')
            return False

        return True
