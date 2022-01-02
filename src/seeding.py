from flask_sqlalchemy import SQLAlchemy


def start_seeding(db: SQLAlchemy):
  seed_roles(db)
  seed_root_user(db)

  seed_admission_types(db)



def seed_roles(db: SQLAlchemy):
  """
  Seeding roles for the app if there is no roles in the DB.
  """
  from .modules.user.user_model import Role

  # check if there is any Root role user
  root_user =  db.session.query(Role).all()

  if len(root_user) == 0:
    print('\nNO ROLES DETECTED, START SEDDING...')

    app_roles = [
      Role(
        name='Quản trị viên',
        code='Administrator',
      ),
      Role(
        name='Người quản lý',
        code='Manager',
      ),
      Role(
        name='Đại sứ',
        code='Envoy',
      ),
    ]

    db.session.add_all(app_roles)
    db.session.commit()


def seed_root_user(db: SQLAlchemy):
  """
  Seeding root user for the app if there is no root role user in the DB.
  """
  from .modules.user.user_model import User

  # check if there is any Root role user
  root_user =  db.session.query(User)\
    .filter(User.role_id == 1)\
    .first()

  # start sedding if there is no Root role user
  if root_user is None:
    print('\nNO ROOT USER DETECTED, START SEDDING...')

    root_user = User(
      first_name='Nguyễn',
      last_name='Anh Tuấn',
      activated=True,
      email='tuanna@student.bvu.edu.vn',
      phone_number='0333326585',
      raw_password='123456',
    )

    root_user.role_id = 1
    db.session.add(root_user)
    db.session.commit()


def seed_admission_types(db: SQLAlchemy):
  """
  Seeding AdmissionType for the app if there is no one.
  """
  from .modules.admission.admission_model import AdmissionType

  if (len(db.session.query(AdmissionType).all()) == 0):
    print('\nNO ADMISSION TYPE DETECTED, START SEDDING...')

    app_admission_types = [
      AdmissionType(name="Đại học chính quy"),
      AdmissionType(name="Liên thông"),
      AdmissionType(name="Thạc sĩ"),
      AdmissionType(name="TIến sĩ"),
    ]

    db.session.add_all(app_admission_types)
    db.session.commit()
