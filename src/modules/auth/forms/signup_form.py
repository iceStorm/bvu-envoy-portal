from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms.fields import StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp, ValidationError, DataRequired

from src.base.helpers.validators import *


def IsEmailExists(form, field):
    from src.modules.user.user_model import User
    if User.query.get(field.data) is not None:
        raise ValidationError(message='The email is already registered')


class SignUpForm(FlaskForm):


    first_name = StringField(
        label='Họ và tên đệm',
        render_kw={'autocomplete': 'name'},
        description={
            'icon': {
                'origin': 'icons/outline/text-outline.svg',
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

    last_name = StringField(
        label='Tên',
        render_kw={'autocomplete': 'name'},
        description={
            'icon': {
                'origin': 'icons/outline/text-outline.svg',
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

    email = EmailField(
        label='Email',
        render_kw={'autocomplete': 'email'},
        description={
            'icon': {
                'origin': 'icons/outline/mail-outline.svg',
            },
        },
        validators=[
            InputRequired(),
            EmailValidator,
            IsEmailExists,
        ]
    )

    phone = StringField(
        label='Số điện thoại',
        render_kw={'autocomplete': 'email'},
        description={
            'icon': {
                'origin': 'icons/outline/keypad-outline.svg',
            },
        },
        validators=[
            InputRequired(),
        ]
    )

    password = PasswordField(
        label='Mật khẩu',
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
        label='Nhập lại mật khẩu',
        render_kw={'autocomplete': 'new-password'},
        description={
            'icon': {
                'origin': 'icons/outline/lock-closed-outline.svg',
                'alternate': 'icons/outline/lock-open-outline.svg',
            },
        },
        validators=[
            InputRequired(message='Please fill out this field'),
            EqualTo(fieldname='password', message='Password fields does not match'),
        ]
    )
