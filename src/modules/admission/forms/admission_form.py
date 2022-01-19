import datetime
from warnings import filters
from flask_wtf import FlaskForm

from wtforms.validators import DataRequired, Length, InputRequired
from wtforms.fields import StringField, IntegerField
from wtforms.fields.html5 import DateTimeLocalField, DateField

from flask_ckeditor import CKEditorField


from ..admission_constants import *
from src.base.helpers.validators import *

from src.main import db
from src.modules.admission.admission_model import Admission
from .fields.rose_field import RoseField
from .fields.admission_types_field import AdmissionTypesField



def validate_name(form, field):
    if form._model:
        if db.session.query(Admission).filter(Admission.name == field.data, Admission.id != form._model.id).first():
            raise ValidationError('This name is already exists')
    elif db.session.query(Admission).filter(Admission.name == field.data).first():
        raise ValidationError('This name is already exists')

def validate_slug(form, field):
    slug_regex_pattern = '([a-z0-9]|\-){5,}'
    if not re.match(slug_regex_pattern, field.data):
        raise ValidationError('Slug format not valid. Allow only ascii, at least 5 letters.')

    if db.session.query(Admission).filter(Admission.slug == field.data).first():
        raise ValidationError('This slug is already exists')


def filter_rose(value: str):
    num = value.replace(',', '').replace('VNĐ', '').strip()
    return num


class AdmissionForm(FlaskForm):
    _model: Admission = None

    name = StringField(
        label='Tên đợt tuyển sinh',
        validators=[
            Length(max=ADMISSION_NAME_LENGTH),
            InputRequired(message='Vui lòng điền vào trường này'),
            validate_name,
        ],
        description={
            'icon': {
                'origin': 'icons/fluent/outline/rename.svg',
            },
        },
        filters=[
            lambda str: str.strip() if str else '',
        ],
    )

    type = AdmissionTypesField(
        label='Đối tượng tuyển sinh',
        validators=[
            DataRequired(),
        ],
        description={
            'icon': {
                'origin': 'icons/fluent/outline/hat_graduation.svg',
            },
        },
    )

    rose = RoseField(
        label='Chiết khẩu (VNĐ)',
        validators=[
            InputRequired(),
        ],
        render_kw={ 'maxlength': 11 },
        description={
            'icon': {
                'origin': 'icons/fluent/outline/people_money.svg',
            },
            'tooltip': 'Số tiền hoa hồng đại sứ nhận được trên mỗi lượt sinh viên nhập học thành công trong chiến dịch này.',
        },
        # filters=[
        #     filter_rose,
        # ],
        post_filters=[
            filter_rose,
        ],
    )

    start_date = DateField(
        label='Thời gian khởi động',
        format='%Y-%m-%d',
        validators=[
            DataRequired(message='Vui lòng điền vào trường này'),
        ],
        description={
            'icon': {
                'origin': 'icons/fluent/outline/calendar_ltr.svg',
            },
        },
    )
    end_date = DateField(
        label='Thời gian kết thúc',
        format='%Y-%m-%d',
        validators=[
            DataRequired(message='Vui lòng điền vào trường này'),
        ],
        description={
            'icon': {
                'origin': 'icons/fluent/outline/calendar_ltr.svg',
            },
        },
    )

    description = CKEditorField(
        label='Mô tả/Chính sách',
        validators=[
            Length(max=ADMISSION_DESCRIPTION_LENGTH),
            InputRequired(message='Vui lòng điền vào trường này'),
        ],
        filters=[
            lambda str: str.strip() if str else '',
        ],
    )


    def validate(self):
        form_passed = True

        begin_datetime = self.start_date.data
        end_datetime = self.end_date.data

        if self.start_date.data and self.end_date.data:
            # check if end time is lower or equal to begin time
            if (end_datetime - begin_datetime).days < 10:
                self.end_date.errors.append('End time must greater than the start time at least 10 days')
                form_passed = False

        form_passed = FlaskForm.validate(self)
        return form_passed
