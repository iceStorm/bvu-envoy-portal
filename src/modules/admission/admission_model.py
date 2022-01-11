from typing import Union
from sqlalchemy import Integer, String, DateTime, Boolean, Column, ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

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
    # slug = Column(String(ADMISSION_SLUG_LENGTH), unique=True, index=True, nullable=False)

    name = Column(String(ADMISSION_NAME_LENGTH), nullable=False, unique=True)
    description = Column(String(length=ADMISSION_DESCRIPTION_LENGTH), nullable=False)
    start_date = Column(Date, nullable=False, index=True)
    end_date = Column(Date, nullable=False, index=True)
    finished = Column(Boolean, default=False, nullable=False)

    type_id = Column(Integer, ForeignKey("AdmissionType.id"), nullable=False)
    type = relationship("AdmissionType", backref="admissions")

    def __init__(self, name: str, type_id: int, description: str, start_date: datetime.date, end_date: datetime.date):
        self.name = name
        # self.slug = slug if slug else self.get_slug_by_name()
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.type_id = type_id


    # def get_slug_by_name(self):
    #     """
    #     Generating slug by name.
    #     """
    #     import unidecode
    #     generated_slug = unidecode.unidecode(self.name.lower().replace(' ', '-'))

    #     # check if the generated_slug is duplicated, appending a ordinay number
    #     while True:
    #         duplicated_slug = db.session.query(Admission).filter(Admission.slug == generated_slug).first()
    #         if duplicated_slug:
    #             generated_slug += '-'
    #         else:
    #             return generated_slug

    @staticmethod
    def get_available_items_to_new_registration():
        """
        Getting list of all available Admissions to clients to register.
        """
        return db.session.query(Admission).filter(
        Admission.finished == False, 
        Admission.end_date >= datetime.datetime.now()
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
    # (student_id, admission_id) count not be same on each record (each student can only subscribe to an envoy in an admission), 
    # means at least they have to be in a composite primary key/composite unique constraint.
    __tablename__ = 'UserAdmission'

    id = Column(Integer, primary_key=True)
    user_joined_time = Column(DateTime, nullable=False,default=datetime.datetime.now())
    student_joined_time = Column(DateTime)

    # user here could be envoy/manager
    user_id = Column(Integer, ForeignKey("User.id", ondelete='CASCADE'), nullable=False)
    user = relationship("User", backref="user_admissions")

    admission_id = Column(Integer, ForeignKey("Admission.id", ondelete='CASCADE'), nullable=False)
    admission = relationship("Admission", backref="user_admissions")

    # applied student to this admission, with this envoy id
    # student id could be null
    student_id = Column(String(ADMISSION_STUDENT_ID_LENGTH))

    __table_args__ = (
        UniqueConstraint(admission_id, student_id),
        {'extend_existing': True, },
    )
