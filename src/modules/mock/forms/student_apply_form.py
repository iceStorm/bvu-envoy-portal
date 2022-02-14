from warnings import filters
from flask_wtf import FlaskForm
from wtforms.fields import IntegerField, StringField
from wtforms.validators import InputRequired, DataRequired

class StudentApplyForm(FlaskForm):
  student_id = IntegerField(
    label='Mã số học viên',
    validators=[
      DataRequired(),
    ],
    description={
      'icon': {
          'origin': 'icons/fluent/outline/mail.svg',
      },
    },
  )

  referral_code = StringField(
    label='Mã giới thiệu đại sứ',
    validators=[
      InputRequired(),
    ],
    description={
      'icon': {
          'origin': 'icons/fluent/outline/mail.svg',
      },
    },
  )
