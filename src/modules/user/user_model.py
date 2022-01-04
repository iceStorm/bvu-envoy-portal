from datetime import datetime
import bcrypt
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from sqlalchemy import String, Integer, Boolean, DateTime, Column, ForeignKey

# from werkzeug.security import generate_password_hash, check_password_hash

from .user_constants import *
from ..envoy.envoy_constants import *

from src.main import db
bcrypt = Bcrypt()

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    __table_args__ = {'extend_existing': True}

    # BASE USER FIELDS ----------------------------------------------------------------------------------------
    id = Column(Integer, primary_key=True)
    email = Column(String(USER_EMAIL_LENGTH), nullable=False, unique=True, index=True)
    phone_number = Column(String(USER_PHONE_LENGTH), nullable=False, unique=True, index=True)
    first_name = Column(String(USER_FIRST_NAME_LENGTH), index=True)
    last_name = Column(String(USER_LAST_NAME_LENGTH), index=True)
    password_hash = Column(String(USER_PASSWORD_LENGTH), nullable=False)
    avatar_url = Column(String(USER_AVATAR_URL_LENGTH))
    username = Column(String(USER_USERNAME_LENGTH), index=True, unique=True)
    activated = Column(Boolean, nullable=False, default=False)
    created_time = Column(DateTime, nullable=False, default=datetime.now())

    # roleId:3 == Envoy
    role_id = Column(Integer, ForeignKey('Role.id'), nullable=False, default=3)
    role = relationship('Role', backref='users')

    # ADDITIONAL ENVOY FIELDS ---------------------------------------------------------------------------------
    address = Column(String(ENVOY_ADDRESS_LENGTH), unique=True, index=True)
    citizen_id = Column(String(ENVOY_CITIZEN_ID_LENGTH), unique=True, index=True)
    credit_card_number = Column(String(ENVOY_CARD_NUMBER_LENGTH), unique=True, index=True)
    organization_tax_id = Column(String(ENVOY_TAX_ID_LENGTH), unique=True, index=True)
    organization_name = Column(String(ENVOY_ORGANIZATION_NAME_LENGTH), unique=True, index=True)
    organization_representer_person_name = Column(String(ENVOY_ORGANIZATION_REPRESENTER_NAME_LENGTH), unique=True, index=True)

    envoy_type_id = Column(Integer, ForeignKey('EnvoyType.id'))
    envoy_type = relationship('EnvoyType', backref='users')


    def __init__(self, email: str, first_name: str, last_name: str, phone_number: str, raw_password=None, avatar_url=None, activated=False):
        """
        Creating a new User instance.
        raw_password: this field will be encrypted automatically.
        """
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.avatar_url = avatar_url
        self.phone_number = phone_number
        self.activated = activated
        self.avatar_url = avatar_url

        # if raw_password provided through the constructor
        if raw_password:
            self.password_hash = User.gen_password_hash(raw_password)
            print(f'hashing the password {raw_password}:', self.password_hash)

    def get_id(self):
        """
        Overriding the get_id to return id - that we used at the primary key. Use for flask-login.
        """
        return self.id

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<User: full name: {self.full_name}, email: {self.email}>"

    @staticmethod
    def gen_password_hash(raw_password):
        # return generate_password_hash(raw_password)
        return bcrypt.generate_password_hash(raw_password)

    def check_password(self, raw_password: str):
        """
        Checking if the raw_password matches the password of this User instance.
        """
        # return check_password_hash(self.password_hash, raw_password)
        return bcrypt.check_password_hash(self.password_hash, raw_password)



class Role(db.Model):
    __tablename__ = 'Role'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(USER_ROLE_LENGTH), nullable=False, unique=True, index=True)
    code = Column(String(USER_ROLE_LENGTH), nullable=False, unique=True, index=True)



class EnvoyType(db.Model):
    __tablename__ = 'EnvoyType'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(ENVOY_TYPE_NAME_LENGTH), nullable=False, unique=True, index=True)
