from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.sql.schema import Column, ForeignKey
from src.main import db

import datetime
from .admission_constants import *


class AdmissionType(db.Model):
  __tablename__ = 'AdmissionTypes'
  __table_args__ = {'extend_existing': True}

  id = Column(Integer, primary_key=True)
  name = Column(String(ADMISSION_NAME_LENGTH), nullable=False, unique=True)



class Admission(db.Model):
  __tablename__ = 'Admissions'
  __table_args__ = {'extend_existing': True}

  id = Column(Integer, primary_key=True)
  name = Column(String(ADMISSION_NAME_LENGTH), nullable=False, unique=True)
  description = Column(TEXT(length=ADMISSION_DESCRIPTION_LENGTH), nullable=False)
  start_time = Column(DateTime, default=datetime.datetime.now(), nullable=False, index=True)
  end_time = Column(DateTime, default=datetime.datetime.now(), nullable=False, index=True)

  type_id = Column(Integer, ForeignKey("AdmissionTypes.id"), nullable=False)
  type = db.relationship("AdmissionType", backref="admissions")
