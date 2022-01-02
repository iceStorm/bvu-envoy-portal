from sqlalchemy.types import Integer, String
from sqlalchemy.sql.schema import Column
from src.main import db

from .admission_constants import *

class Admission(db.Model):
  __tablename__ = 'Admissions'
  __table_args__ = {'extend_existing': True}

  id = Column(Integer, primary_key=True)
  name = Column(String(ADMISSION_NAME_LENGTH), nullable=False, unique=True)
  descriptions = Column(String(ADMISSION_DESCRIPTION_LENGTH), nullable=False)
