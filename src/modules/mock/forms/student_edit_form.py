from warnings import filters
from flask_wtf import FlaskForm
from wtforms.fields import IntegerField, StringField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import InputRequired, DataRequired, Optional

class StudentEditForm(FlaskForm):
  referral_code = StringField(
    label='Mã giới thiệu đại sứ',
    description={
      'icon': {
          'origin': 'icons/fluent/outline/number.svg',
      },
    },
    render_kw={ "disabled": "true" },
  )

  envoy_name = StringField(
    label='Tên đại sứ',
    description={
      'icon': {
          'origin': 'icons/fluent/outline/person.svg',
      },
    },
    render_kw={ "disabled": "true" },
  )

  envoy_contact = StringField(
    label='Thông tin liên hệ đại sứ',
    description={
      'icon': {
          'origin': 'icons/fluent/outline/mail.svg',
      },
    },
    render_kw={ "disabled": "true" },
  )

  student_id = IntegerField(
    label='Mã số học viên',
    description={
      'icon': {
          'origin': 'icons/fluent/outline/number.svg',
      },
    },
    render_kw={ "disabled": "true" },
  )

  applied_time = DateTimeLocalField(
    label='Thời gian đăng ký',
    render_kw={ "disabled": "true" },
    format='%Y-%m-%dT%H:%M',
    description={
      'icon': {
          'origin': 'icons/fluent/outline/calendar_ltr.svg',
      },
    },
  )

  paid_time = DateTimeLocalField(
    label='Thời gian nhập học',
    format='%Y-%m-%dT%H:%M',
    description={
      'icon': {
          'origin': 'icons/fluent/outline/calendar_ltr.svg',
      },
    },
  )
