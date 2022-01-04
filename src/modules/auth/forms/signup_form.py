from flask_wtf import FlaskForm
from wtforms.fields.core import IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.fields import StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp, ValidationError, DataRequired

from src.base.helpers.validators import *


def IsEmailExists(form, field):
    from src.modules.user.user_model import User, db
    if db.session.query(User).filter(User.email == field.data).first() is not None:
        raise ValidationError(message='The email is already registered')


class SignUpForm(FlaskForm):
    organization_name = StringField(
        label='Tên Tổ chức/Công ty/Trường học',
        render_kw={'autocomplete': 'organization'},
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

    organization_representer_person_name = StringField(
        label='Tên người đại diện',
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

    organization_tax_id = IntegerField(
        label='Mã số thuế',
        render_kw={'autocomplete': 'new-password'},
        description={
            'icon': {
                'origin': 'icons/outline/lock-closed-outline.svg',
                'alternate': 'icons/outline/lock-open-outline.svg',
            },
        },
        validators=[
            DataRequired(message='Please fill out this field'),
        ]
    )

    address = StringField(
        label='Địa chỉ',
        render_kw={'autocomplete': 'address-line1'},
        description={
            'icon': {
                'origin': 'icons/outline/locate-outline.svg',
            },
        },
        validators=[
            InputRequired(),
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
        render_kw={'autocomplete': 'tel'},
        description={
            'icon': {
                'origin': 'icons/outline/keypad-outline.svg',
            },
        },
        validators=[
            InputRequired(),
        ]
    )