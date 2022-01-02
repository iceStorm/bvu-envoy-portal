from flask_wtf import FlaskForm

from wtforms.validators import DataRequired, Length
from wtforms.fields import StringField
from wtforms.fields.html5 import DateTimeLocalField

from ..admission_constants import *


class AdmissionForm(FlaskForm):
  name = StringField(
    label='Tên đợt tuyển sinh',
    validators=[
      Length(max=ADMISSION_NAME_LENGTH),
      DataRequired(message='Vui lòng điền vào trường này'),
    ],
    filters=[
      lambda str: str.strip(),
    ],
  )

  description = StringField(
    label='Mô tả/Chính sách',
    validators=[
      Length(max=ADMISSION_DESCRIPTION_LENGTH),
      DataRequired(message='Vui lòng điền vào trường này'),
    ],
    filters=[
      lambda str: str.strip(),
    ],
  )

  start_date = DateTimeLocalField(
    label='Thời gian khởi động',
    validators=[
      DataRequired(message='Vui lòng điền vào trường này'),
    ],
    filters=[
      lambda str: str.strip(),
    ],
  )
  end_date = DateTimeLocalField(
    label='Thời gian kết thúc',
    validators=[
      DataRequired(message='Vui lòng điền vào trường này'),
    ],
    filters=[
      lambda str: str.strip(),
    ],
  )


  from .fields.admission_types_field import AdmissionTypesField
  type = AdmissionTypesField(validators=[
    DataRequired(),
  ])
