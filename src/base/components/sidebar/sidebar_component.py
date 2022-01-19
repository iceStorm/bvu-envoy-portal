from flask import request, render_template, current_app
from flask.helpers import url_for
from flask_login import current_user

from .sidebar_viewmodel import NavBarViewModel, NavItem, NavItemIcon, NavItemGroup

# import this model to handle the DB (Flask-SQLAlchemy)
from src.modules.user.user_model import User
from src.modules.admission.admission_model import Admission
from src.main import logger, db
from .role_viewmodels import *

def get_view_model() -> NavBarViewModel:
    """
    Resetting the nav items active state, load the current_user
    """
    print('\ncurrent_user inside NavBar component:', current_user.id)

    nav_item_groups = admin_sidebar() if current_user.role.code == 'admin' \
            else manager_sidebar() if current_user.role.code == 'manager' \
                else envoy_sidebar()

    return NavBarViewModel(
        nav_item_groups=nav_item_groups,
    )


def sidebar_component():
    def component():
        # getting a new view model instance
        vm = get_view_model()

        # getting current requesting path
        req_path = request.path
        print('req path:', req_path)

        # setting the current active page
        vm.set_active_nav_item(path=req_path)
        
        return render_template("components/user/sidebar.html", vm=vm)

    return dict(SidebarComponent=component)
