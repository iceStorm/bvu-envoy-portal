from wtforms import SelectField


class AdmissionTypesField(SelectField):
  # **kwargs is always required
    def __init__(self, **kwargs):
        super(AdmissionTypesField, self).__init__(**kwargs)


        # data type
        self.coerce = int

        # html label tag
        self.label.text = 'Đối tượng tuyển sinh'

        # filling the choices for this SelectField
        # getting projects belog to this user (logged in user)
        from src.modules.admission.admission_model import AdmissionType
        from src.main import db
        
        self.choices = [(ams.id, ams.name) for ams in db.session.query(AdmissionType).all()]

