import os

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from src.app import db
from src.main.modules.user.user_model import User
from src.main.modules.auth.forms.signup_form import SignUpForm


class AuthService:
    @staticmethod
    def send_reset_password_email(email: str) -> None:
        raise Exception("The email is not exists on the system")


    @staticmethod
    def is_user_already_exists(email):
        return User.query.get(email) is not None


    @staticmethod
    def register(form: SignUpForm):
        email = form.email.data
        fullName = form.full_name.data
        password = form.password.data

        # creating a new user based-on the Form's data
        # the user's password auto encrypted via the User's constructor
        new_user = User(email=email, full_name=fullName, raw_password=password)

        db.session.add(new_user)
        db.session.commit()


    @staticmethod
    def update(email: str, user: User):
        the_user = User.query.get(email)
        the_user.full_name = user.full_name

        # checking if the avatar is modified
        print('avatar_path:', user.avatar_url)

        if user.avatar_url == 'null': # when the user removes avatar --> also remove in the DB record
            print('resetting the avatar_url...')
            the_user.avatar_url = None
        elif user.avatar_url is not None:   # when the user uploads a new avatar
            # deleting the old avatar if exists
            if the_user.avatar_url: # make sure the user's avatar is exists in the DB (not None)
                if os.path.isfile(the_user.avatar_url): # make sure the file is exists on the file system
                    os.unlink(the_user.avatar_url)
                    print('removed the old avatar: %s\n' % the_user.avatar_url)

            # assigning the new avatar url to the user
            the_user.avatar_url = user.avatar_url

        db.session.commit()


    @staticmethod
    def save_avatar_image(form_image_data: FileStorage) -> str:
        the_path = ''

        if form_image_data:
            the_avatar_name = secure_filename(filename=form_image_data.filename)

            # saving the avatar image
            print('current_app.instance_path:', current_app.instance_path)
            the_path = os.path.abspath(
                os.path.join(
                    current_app.instance_path,
                    'main/base/static/users/avatars',
                    the_avatar_name,
                )
            )

            the_path = '/'.join(the_path.split('\\'))
            form_image_data.save(the_path)

        # returning the saved image path
        return the_path
