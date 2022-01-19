from flask_wtf import FlaskForm, RecaptchaField

from wtforms.fields.html5 import EmailField
from wtforms.fields import StringField, PasswordField, IntegerField, RadioField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp, ValidationError, DataRequired, Required, Optional

from src.modules.user.user_constants import *
from src.modules.envoy.envoy_constants import *
from src.base.helpers.validators import *


def IsEmailExists(form, field):
    from src.modules.user.user_model import User, db
    if db.session.query(User).filter(User.email == field.data).first() is not None:
        raise ValidationError(message='The email is already registered')


class SignUpForm(FlaskForm):
    envoy_type = RadioField(
        coerce=int,
        choices=[
            (0, 'Cơ quan/Tổ chức/Trường học'),
            (1, 'Cá nhân thuộc tập đoàn NHG (Sinh viên, giảng viên, nhân viên)'),
        ],
        validators=[
            InputRequired(),
        ],
    )

    organization_name = StringField(
        label='Tên Tổ chức/Công ty/Trường học',
        render_kw={'autocomplete': 'organization', 'maxlength': ENVOY_ORGANIZATION_NAME_LENGTH,},
        description={
            'icon': {
                'origin': 'icons/fluent/outline/building.svg',
            },
            'tooltip': 'Ví dụ: Trường THPT chuyên Lê Quý Đôn',
        },
        filters=[
            lambda string: str(string).strip() if string else '',   # discarding all redundant spaces
        ],
        validators=[
            InputRequired(message='Please fill out this field'),
            Length(min=10, max=ENVOY_ORGANIZATION_NAME_LENGTH, 
            message=f'The length must between 10 and {ENVOY_ORGANIZATION_NAME_LENGTH} letters'),
        ]
    )

    organization_representer_person_name = StringField(
        label='Tên người đại diện',
        render_kw={'autocomplete': 'name', 'maxlength': ENVOY_ORGANIZATION_REPRESENTER_NAME_LENGTH,},
        description={
            'icon': {
                'origin': 'icons/fluent/outline/person.svg',
            },
            'tooltip': 'Tên người đại diện cho tổ chức',
        },
        filters=[
            lambda string: str(string).strip() if string else '',   # discarding all redundant spaces
        ],
        validators=[
            InputRequired(message='Please fill out this field'),
            Length(min=10, max=ENVOY_ORGANIZATION_REPRESENTER_NAME_LENGTH,
            message=f'The length must between 10 and {ENVOY_ORGANIZATION_REPRESENTER_NAME_LENGTH} letters'),
        ]
    )

    organization_tax_id = StringField(
        label='Mã số thuế',
        render_kw={'autocomplete': 'new-password', 'maxlength': ENVOY_TAX_ID_LENGTH,},
        description={
            'icon': {
                'origin': 'icons/fluent/outline/hash.svg',
            },
            'tooltip': """Mã số thuế gồm 10 hoặc 13 chữ số.
                <a href="https://luatminhkhue.vn/quy-dinh-ve-ma-so-thue-va-y-nghia-cac-con-so-theo-quy-dinh-cua-luat.aspx"
                    class="link text-primary underline"
                    target="_blank">
                    Tham khảo tại đây.
                </a>""",
        },
        filters=[
            lambda string: str(string).strip() if string else '',   # discarding all redundant spaces
        ],
        validators=[
            InputRequired(message='Please fill out this field'),
            TaxIdValidator,
        ],
    )

    citizen_id = StringField(
        label='Số CCCD/CMND của người đại diện',
        render_kw={'autocomplete': 'new-password', 'maxlength': ENVOY_CITIZEN_ID_LENGTH,},
        description={
            'icon': {
                'origin': 'icons/fluent/outline/person-card.svg',
            },
            'tooltip': 'Số Chứng minh nhân dân (9 chữ số) hoặc Số Căn cước công dân (12 chữ số).',
        },
        filters=[
            lambda string: str(string).strip() if string else '',   # discarding all redundant spaces
        ],
        validators=[
            InputRequired(message='Please fill out this field'),
            CitizenIdValidator,
        ]
    )

    email = EmailField(
        label='Email',
        render_kw={'autocomplete': 'email', 'maxlength': USER_EMAIL_LENGTH,},
        description={
            'icon': {
                'origin': 'icons/fluent/outline/mail.svg',
            },
            'tooltip': """Kiểm tra định dạng email của bạn
                <a href="https://regex101.com/r/tYNbwr/1"
                    class="link text-primary underline" target="_blank">
                    tại đây.
                </a>""",
        },
        filters=[
            lambda string: str(string).strip() if string else '',   # discarding all redundant spaces
        ],
        validators=[
            InputRequired(),
            EmailValidator,
        ]
    )

    phone = StringField(
        label='Số điện thoại',
        render_kw={'autocomplete': 'tel', 'maxlength': USER_PHONE_LENGTH,},
        description={
            'icon': {
                'origin': 'icons/fluent/outline/number.svg',
            },
            'tooltip': 'Số điện thoại gồm 10 hoặc 11 chữ số.',
        },
        filters=[
            lambda string: str(string).strip() if string else '',   # discarding all redundant spaces
        ],
        validators=[
            InputRequired(),
            PhoneNumberValidator,
        ]
    )

    address = StringField(
        label='Địa chỉ',
        render_kw={'autocomplete': 'address-line1', 'maxlength': ENVOY_ADDRESS_LENGTH,},
        description={
            'icon': {
                'origin': 'icons/fluent/outline/location.svg',
            },
        },
        filters=[
            lambda string: str(string).strip() if string else '',   # discarding all redundant spaces
        ],
        validators=[
            InputRequired(),
        ]
    )

    recaptcha = RecaptchaField(
        # label='Chọn vào ô sau',
        validators=[
            # InputRequired(message='Please tick the captcha'),
        ],
    )


    def validate(self):
        # first, validate the above requirements by: passing this instance to the FlaskForm.validate()
        # ensure all fields are filled
        if not FlaskForm.validate(self):
            return False
        
        form_passed = True
        from src.modules.user.user_model import User

        if User.is_email_already_exists(self.email.data):
            self.email.errors.append('This email already exists')
            form_passed = False

        if User.is_phone_already_exists(self.phone.data):
            self.phone.errors.append('This phone number already exists')
            form_passed = False

        if User.is_organization_name_already_exists(self.organization_name.data):
            self.organization_name.errors.append('This organization name already exists')
            form_passed = False
        
        if User.is_organization_representer_name_already_exists(self.organization_representer_person_name.data):
            self.organization_representer_person_name.errors.append('This representer name already exists')
            form_passed = False

        if User.is_organization_taxid_already_exists(self.organization_tax_id.data):
            self.organization_tax_id.errors.append('This tax id already exists')
            form_passed = False

        if User.is_citizen_id_already_exists(self.citizen_id.data):
            self.citizen_id.errors.append('This citizen id already exists')
            form_passed = False

        if User.is_address_already_exists(self.address.data):
            self.address.errors.append('This address already exists')
            form_passed = False

        # awalys return True
        return form_passed

