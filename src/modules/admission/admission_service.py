from .admission_model import Admission
from src.main import db, logger

class AdmissionService:
  @staticmethod
  def add(model: Admission) -> bool:
    try:
      db.session.add(model)
      db.session.commit()
      return True
    except Exception as e:
      logger.exception(e)
      db.session.rollback()
      return False

  @staticmethod
  def update(old_model: Admission, desired_model: Admission) -> bool:
    # try:
    #   db.session.commit()
    #   return True
    # except Exception as e:
    #   logger.exception(e)
    #   db.session.rollback()
    #   return False
    raise Exception(NotImplementedError())

  @staticmethod
  def update(model: Admission) -> bool:
    try:
      db.session.delete(model)
      db.session.commit()
      return True
    except Exception as e:
      logger.exception(e)
      db.session.rollback()
      return False
