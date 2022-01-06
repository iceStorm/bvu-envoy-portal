from sqlalchemy import Integer, String, DateTime, Boolean, Column, ForeignKey
from sqlalchemy.dialects.mysql import TEXT
from src.main import db

import datetime
from .admission_constants import *


class AdmissionType(db.Model):
  __tablename__ = 'AdmissionType'
  __table_args__ = {'extend_existing': True}

  id = Column(Integer, primary_key=True)
  name = Column(String(ADMISSION_NAME_LENGTH), nullable=False, unique=True)

  @staticmethod
  def is_admission_type_name_already_exists(self, name: str):
    """
    Check whether the given :name is already in the DB.
    """
    return db.session.query(AdmissionType).filter(AdmissionType.name == name).first() is not None


class Admission(db.Model):
  __tablename__ = 'Admission'
  __table_args__ = {'extend_existing': True}

  id = Column(Integer, primary_key=True)
  name = Column(String(ADMISSION_NAME_LENGTH), nullable=False, unique=True)
  description = Column(String(length=ADMISSION_DESCRIPTION_LENGTH), nullable=False)
  start_time = Column(DateTime, default=datetime.datetime.now(), nullable=False, index=True)
  end_time = Column(DateTime, default=datetime.datetime.now(), nullable=False, index=True)
  finished = Column(Boolean, default=False, nullable=False)

  type_id = Column(Integer, ForeignKey("AdmissionType.id"), nullable=False)
  type = db.relationship("AdmissionType", backref="admissions")

  @staticmethod
  def get_available_items_to_new_registration():
    """
    Getting list of all available Admissions to clients to register.
    """
    return db.session.query(Admission).filter(
      Admission.finished == False, 
      Admission.end_time > datetime.datetime.now()
    ).all()

  @staticmethod
  def finished_items(self):
    """
    Getting all finished admissions.
    """
    return db.session.query(Admission).filter(Admission.finished == True).all()
  
  @staticmethod
  def running_items(self):
    """
    Getting all closed but not finished admissions (on hold for handling bonus for envoy...).
    """
    return db.session.query(Admission).filter(Admission.finished == False).all()


class UserAdmission(db.Model):
    __tablename__ = 'UserAdmission'
    __table_args__ = {'extend_existing': True}

    user_id = Column(Integer, ForeignKey("User.id"), nullable=False, primary_key=True)
    user = db.relationship("User", backref="user_admissions")

    admission_id = Column(Integer, ForeignKey("Admission.id"), nullable=False, primary_key=True)
    admission = db.relationship("Admission", backref="user_admissions")

