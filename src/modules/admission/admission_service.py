from .admission_model import Admission, AdmissionPresenter
from src.main import db, logger
from .forms.admission_form import AdmissionForm

class AdmissionService:
  @staticmethod
  def add(model: Admission):
    try:
      db.session.add(model)
      db.session.commit()
      return model
    except Exception as e:
      logger.exception(e)
      db.session.rollback()
      return None


  @staticmethod
  def update(old_model: Admission, form: AdmissionForm):
    try:
      old_model.name = form.name.data
      old_model.description = form.description.data
      # old_model.slug = form.slug.data
      old_model.start_date = form.start_date.data
      old_model.end_date = form.end_date.data
      old_model.type_id = form.type.data
      old_model.rose = form.rose.data
      db.session.commit()
      return True
    except Exception as e:
      logger.exception(e)
      db.session.rollback()
      return False


  @staticmethod
  def delete(model: Admission) -> bool:
    try:
      db.session.delete(model)
      db.session.commit()
      return True
    except Exception as e:
      logger.exception(e)
      db.session.rollback()
      return False


  @staticmethod
  def mark_done(model: Admission, revoke=False):
    try:
      model.finished = True if not revoke else False
      db.session.commit()
      return True
    except Exception as e:
      logger.exception(e)
      db.session.rollback()
      return False


  @staticmethod
  def apply_student(student_id: str, user_admission: AdmissionPresenter):
    try:
      user_admission.students.add()
      db.session.commit()
      return True
    except Exception as e:
      logger.exception(e)
      db.session.rollback()
      return False
