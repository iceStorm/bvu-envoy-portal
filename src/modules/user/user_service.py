from datetime import datetime
from src.main import db, logger
from src.modules.user.user_model import User


class UserService:

    @staticmethod
    def activate(user: User):
        """
        Kích hoạt lại tài khoản đã khóa trước đó.
        """
        try:
            user.activated = True
            db.session.commit()
            return True
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            return False
    

    @staticmethod
    def deactivate(user: User):
        """
        Bỏ kích hoạt lại tài khoản đã khóa trước đó.
        """
        try:
            user.activated = False
            db.session.commit()
            return True
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            return False
    
    
    @staticmethod
    def verify(user: User):
        """
        Xác thực lần đầu tài khoản đại sứ.
        """
        try:
            user.activated = True
            user.verified_time = datetime.now()
            db.session.commit()
            return True
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            return False
