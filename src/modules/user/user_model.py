from sqlalchemy.orm import relationship
from flask_login import UserMixin
from sqlalchemy import Sequence
from sqlalchemy.sql.schema import ForeignKey

from werkzeug.security import generate_password_hash, check_password_hash

from src.base.constants.user_constants import *
from src.main import db


class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    __table_args__ = {'extend_existing': True}

    # base user fields
    id = db.Column(db.Integer, primary_key=True, index=True)
    email = db.Column(db.String(USER_EMAIL_LENGTH), index=True)
    phone_number = db.Column(db.String(USER_PHONE_LENGTH), nullable=False, index=True)
    first_name = db.Column(db.String(USER_FIRST_NAME_LENGTH), nullable=False, index=True)
    last_name = db.Column(db.String(USER_LAST_NAME_LENGTH), nullable=False, index=True) 
    password_hash = db.Column(db.String(USER_PASSWORD_LENGTH), nullable=False)
    avatar_url = db.Column(db.String(USER_AVATAR_URL_LENGTH))



    def __init__(self, email=None, full_name=None, raw_password=None, avatar_url=None):
        """
        Creating a new User instance.
        raw_password: this field will be encrypted automatically.
        """
        self.email = email
        self.full_name = full_name
        self.avatar_url = avatar_url

        # if raw_password provided through the constructor
        if raw_password:
            password_hash = User.gen_password_hash(raw_password)
            print(f'hashing the password {raw_password}:', password_hash)
            self.password_hash = password_hash


    @staticmethod
    def gen_password_hash(raw_password):
        return generate_password_hash(raw_password)


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


    def check_password(self, raw_password: str):
        """
        Checking if the raw_password matches the password of this User instance.
        """
        return check_password_hash(self.password_hash, raw_password)




class Role(db.Model):
    __tablename__ = 'Roles'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(USER_ROLE_LENGTH), nullable=False, unique=True)


class UserRole(db.Model):
    __tablename__ = 'UserRoles'
    __table_args__ = {'extend_existing': True}

    role_id = db.Column(db.Integer, ForeignKey('Roles.id'), primary_key=True,)
    role = relationship('Role', backref='user_roles')

    user_id = db.Column(db.Integer, ForeignKey('Users.id'), primary_key=True,)
    user = relationship('User', backref='user_roles')
