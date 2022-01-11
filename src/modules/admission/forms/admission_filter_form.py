import datetime
from flask_wtf import FlaskForm
from wtforms.fields.core import SelectField

from wtforms.validators import DataRequired, Length, InputRequired, Optional
from wtforms.fields import StringField, DateTimeField
from wtforms.fields.html5 import DateTimeLocalField, DateField

from flask_ckeditor import CKEditorField

from .fields.admission_types_field import AdmissionTypesField
from ..admission_constants import *


class AdmissionFilterForm(FlaskForm):
    type = AdmissionTypesField(
        show_all_option=True,
        label='Đối tượng tuyển sinh',
        validators=[
        ],
        description={
        'icon': {
            'origin': 'icons/fluent/outline/hat_graduation.svg',
        },
        'tooltip': 'Số điện thoại gồm 10 hoặc 11 chữ số.',
        },
    )

    start_date = DateField(
        label='Ngày khởi động',
        format='%Y-%m-%d',
        validators=[
            Optional(),
        ],
        description={
        'icon': {
            'origin': 'icons/fluent/outline/calendar_ltr.svg',
        },
        'tooltip': 'Số điện thoại gồm 10 hoặc 11 chữ số.',
        },
    )
    end_date = DateField(
        label='Ngày kết thúc',
        format='%Y-%m-%d',
        validators=[
            Optional(),
        ],
        description={
        'icon': {
            'origin': 'icons/fluent/outline/calendar_ltr.svg',
        },
        'tooltip': 'Số điện thoại gồm 10 hoặc 11 chữ số.',
        },
    )

    max_per_page = SelectField(
        label='Hiển thị',
        coerce=int,
        validators=[
        ],
        choices=[
            (6, '6'),
            (12, '12'),
            (18, '18'),
        ],
        description={
        'icon': {
            'origin': 'icons/fluent/outline/grid_dots.svg',
        },
        'tooltip': 'Số điện thoại gồm 10 hoặc 11 chữ số.',
        },
    )


    def validate(self):
        if not FlaskForm.validate(self):
            return False

        form_passed = True

        begin_datetime = self.start_date.data
        end_datetime = self.end_date.data

        from src.main import db
        from src.modules.admission.admission_model import Admission

        # check if end time is lower or equal to begin time
        if end_datetime and begin_datetime:
            if (end_datetime - begin_datetime).days <= 0:
                self.end_date.errors.append('End time must greater than the start time')
                form_passed = False
        
        return form_passed
