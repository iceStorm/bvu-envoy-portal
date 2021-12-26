from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms.fields import StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp, ValidationError, DataRequired

from src.main.base.helpers.validators import *


def IsEmailExists(form, field):
    from src.main.modules.user.user_model import User
    if User.query.get(field.data) is not None:
        raise ValidationError(message='The email is already registered')


class SignUpForm(FlaskForm):
    email = EmailField(
        label='Email',
        render_kw={'autocomplete': 'email'},
        description={
            'icon': {
                'origin': 'icons/outline/finger-print-outline.svg',
            },
        },
        validators=[
            InputRequired(),
            EmailValidator,
            IsEmailExists,
        ]
    )

    full_name = StringField(
        label='Full name',
        render_kw={'autocomplete': 'name'},
        description={
            'icon': {
                'origin': 'icons/outline/scan-outline.svg',
            },
        },
        filters=[
            lambda string: str(string).strip() if string else '',   # discarding all redundant spaces
        ],
        validators=[
            DataRequired(message='Please fill out this field'),
            Length(min=2, max=50, message='The length must between 2 and 50 letters'),
        ]
    )

    password = PasswordField(
        label='Password',
        render_kw={'autocomplete': 'new-password'},
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

    re_password = PasswordField(
        label='Re-enter password',
        render_kw={'autocomplete': 'new-password'},
        description={
            'icon': {
                'origin': 'icons/outline/lock-closed-outline.svg',
                'alternate': 'icons/outline/lock-open-outline.svg',
            },
        },
        validators=[
            InputRequired(message='Please fill out this field'),
            PasswordValidator,
            EqualTo(fieldname='password', message='Password fields does not match'),
        ]
    )
