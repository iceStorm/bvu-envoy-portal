from typing import List
from wtforms import IntegerField

from src.modules.admission.admission_model import AdmissionType
from src.main import db


class RoseField(IntegerField):
    # **kwargs is always required
    def __init__(self, post_filters=[], **kwargs):
        super(RoseField, self).__init__(**kwargs)
        self.post_filters = post_filters

    def process_formdata(self, valuelist):
        """
        Put your filter on the form data (user input - not sanitized) logics here
        """
        data = valuelist[0]

        for filter in self.post_filters:
            data = filter(data)

        return super(RoseField, self).process_formdata([data])
