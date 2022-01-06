"""
Entrypoint of the application.
"""

import sys
import os
from pathlib import Path

from .App import App


# CONFIG LOGGER
import logging as logger
logger.basicConfig(format='%(asctime)s - %(message)s', level=logger.INFO,)


# INIT DATABASE
print("\n[DEFINING DATABASE INSTANCE...]")
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


# INIT RATE LIMITING
print("\n[DEFINING RATE LIMITING INSTANCE...]")
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
limiter = Limiter(key_func=get_remote_address)


# INIT MAIL
from flask_mail import Mail
mail = Mail()


# principals
from flask_principal import Principal, Permission, RoleNeed, UserNeed, identity_loaded
principals = Principal()
# declaring permission Needs
admin_permission = Permission(RoleNeed('admin'))
manager_permission = Permission(RoleNeed('manager'), RoleNeed('admin'))
envoy_permission = Permission(RoleNeed('envoy'), RoleNeed('manager'), RoleNeed('admin'))



def add_sys_paths():
    print('\n[ADDING PATHS TO THE PYTHON ENVIRONMENT...]')

    # getting the current file's absolute path
    CURRENT_FILE_ABSOLUTE_PATH = Path(__file__).absolute()

    # WORKING_DIR: src
    WORKING_DIR = os.path.abspath(os.path.join(CURRENT_FILE_ABSOLUTE_PATH, '../'))

    # ROOT_DIR (includes the: src ; scripts ; venv ; ..
    ROOT_DIR = os.path.abspath(os.path.join(CURRENT_FILE_ABSOLUTE_PATH, '../../'))

    # appending the WORKING_DIR, ROOT_DIR to the python environment
    sys.path.append(WORKING_DIR)
    # sys.path.append(ROOT_DIR)
    print('\n[PATHS IN THE PYTHON ENVIRONMENT...]:')
    print('\n'.join(sys.path), '\n')

    return WORKING_DIR, ROOT_DIR


def init_db(app: App):
    """
    Initializing DB connnection.
    Migrating models to DB schema/tables.
    Seeding initial data.
    """
    db.init_app(app=app)

    # MIGRATING MODELS TO DB SCHEMAS
    from flask_migrate import Migrate
    print("\n\n[MIGRATING THE DATABASE...]")
    migrate = Migrate()
    with app.app_context():
        # allow dropping column for sqlite
        if db.engine.url.drivername == 'sqlite':
            migrate.init_app(app, db, render_as_batch=True)
        else:
            migrate.init_app(app, db)

    # IMPORTING MODELS IS NEEDED FOR FLASK-MIGRATE TO DETECT CHANGES
    from .modules.admission.admission_model import Admission
    # from .modules.user.user_model import User

    # START SEEDING INITIAL DATA
    with app.app_context():
        from .seeding import start_seeding
        start_seeding(db)


def init_protections(app: App):
    """
    Initializing application's protection/security extensions.
    """
    limiter.init_app(app)
    # rbac.init_app(app)


def init_principal_user_provider(app: App):
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        from flask_login import current_user

        # Set the identity user object
        identity.user = current_user

        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Add the RoleNeed to the identity
        if hasattr(current_user, 'role'):
            identity.provides.add(RoleNeed(current_user.role.code))


def hooks(app: App):
    """
    Defining hook operations.
    """
    @app.before_request
    def app_before_request():
        pass
        

def create_app():
    """
    Initializing the App and plug-in extensions.
    Return a runnable Flask application.
    """
    print("\n[INITIALIZING THE APP...]")
    app = App()

    init_db(app=app)
    init_protections(app=app)
    mail.init_app(app)

    principals.init_app(app)
    init_principal_user_provider(app)

    hooks(app=app)

    print('\n\n[NEW APP RETURNED...]')
    return app

