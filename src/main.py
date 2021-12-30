"""
Entrypoint of the application.
"""

import sys
import os
from pathlib import Path


# INIT DATABASE
print("\n[DEFINING DATABASE INSTANCE...]")
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


# INIT RATE LIMITING
print("\n[DEFINING RATE LIMITING INSTANCE...]")
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
limiter = Limiter(key_func=get_remote_address)


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


def create_app():
    print("\n[INITIALIZING THE APP...]")
    from .App import App
    # app = App(instance_path=add_sys_paths()[0])
    app = App()

    db.init_app(app=app)
    limiter.init_app(app)
    # rbac.init_app(app)


    # migrating Models to DB
    from flask_migrate import Migrate
    print("\n\n[MIGRATING THE DATABASE...]")
    migrate = Migrate()
    with app.app_context():
        # allow dropping column for sqlite
        if db.engine.url.drivername == 'sqlite':
            migrate.init_app(app, db, render_as_batch=True)
        else:
            migrate.init_app(app, db)

    # importing all model (tables) is needed for flask-migrate to detect changes
    # import main.modules.user.user_model # no need to import the User model, which causing circular importing to relationships
    # import main.modules.project.project_model
    # import main.modules.task.task_model
    # import main.modules.priority.priority_model
    # import main.modules.status.status_model
    # import main.modules.project.project_model

    print('\n\n[NEW APP RETURNED...]')
    return app
