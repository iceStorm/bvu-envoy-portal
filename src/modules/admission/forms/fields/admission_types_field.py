from wtforms import SelectField

from src.modules.admission.admission_model import AdmissionType
from src.main import db


class AdmissionTypesField(SelectField):
    # **kwargs is always required
    def __init__(self, show_all_option=False, **kwargs):
        super(AdmissionTypesField, self).__init__(**kwargs)
        self.show_all_option = show_all_option

        # data type
        self.coerce = int
        self.choices = [(ams.id, ams.name) for ams in db.session.query(AdmissionType).all()]

        if show_all_option:
            self.choices.insert(0, (0, 'Tất cả'))


    # we actually dont need to check this condition
    # def post_validate(self, form, validation_stopped):
    #     available_value = ([ams.id for ams in db.session.query(AdmissionType).all()] + ([0] if self.show_all_option else []))

    #     if self.data not in available_value:
    #         self.errors.append('Selected value does not exist')
