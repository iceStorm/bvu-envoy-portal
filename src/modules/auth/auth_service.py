import os, uuid
import bcrypt

from flask import current_app, session
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from src.main import db, logger
from src.modules.user.user_model import User
from src.modules.auth.forms.signup_form import SignUpForm


class AuthService:
    @staticmethod
    def get_user_from_email(email: str):
        return db.session.query(User).filter_by(email = email).first()

    def get_user_from_username(username: str):
        return db.session.query(User).filter_by(username = username).first()

    @staticmethod
    def send_reset_password_email(email: str) -> None:
        raise Exception(NotImplementedError)

    @staticmethod
    def is_user_already_exists(email):
        print(f'Checking user exists on the system: {email}');
        print(db.session.query(User).filter_by(email = email).first())
        return db.session.query(User).filter_by(email = email).first() is not None

    @staticmethod
    def is_user_activated(email):
        print(f'Checking user account activated on the system: {email}');
        return db.session.query(User).filter(User.email == email, User.activated == True).first() is not None


    @staticmethod
    def register(new_user: User):
        try:
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            return None


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


    @staticmethod
    async def send_register_confirm_email(receiver_email: str, receiver_name: str, code: str):
        from flask_mail import Message
        from src.main import mail
        msg = Message(f'Xác minh đăng ký tài khoản Đại sứ BVU', sender = current_app.config['MAIL_USERNAME'], recipients = [receiver_email])
        msg.html = f"""
        Xin chào {receiver_name},<br /><br />
        Đây là tin nhắn tự động được gửi từ hệ thống Cổng thông tin Đại sứ BVU.<br/>
        Vui lòng sao chép mã sau đây để hoàn tất quá trình đăng ký:
        <h1>{code}</h1>
        """
        await mail.send(msg)

    @staticmethod
    def gen_registration_code() -> str:
        """
        Generating envoy registration code to send to email.
        """
        # getting 6 letters code
        code = ''.join(uuid.uuid1().hex.split('-'))[:6]
        return code
