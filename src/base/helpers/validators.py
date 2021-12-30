from wtforms.validators import Regexp, ValidationError
import re


EmailValidator = Regexp(
    regex='^[a-z][a-z0-9_\.]{5,32}@[a-z0-9]{2,}(\.[a-z0-9]{2,4}){1,2}$',
    message='The email format is invalid'
)


def PasswordValidator(form, field):
    """
    Base password validator for the application.
    @param form:
    @param field:
    """
    if len(field.data) < 6 or len(field.data) > 50:
        raise ValidationError(message='The password must between 6 and 50 characters')
    else:
        password_regex_pattern = '[a-zA-Z0-9]'
        if not re.match(password_regex_pattern, field.data):
            raise ValidationError(message='The password can only contains numbers, letters')

