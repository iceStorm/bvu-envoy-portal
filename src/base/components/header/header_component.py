from flask import request, render_template
from flask_login import current_user

from .header_viewmodel import NavBarViewModel, NavItem, NavItemIcon

# import this model to handle the DB (Flask-SQLAlchemy)
from src.modules.user.user_model import User
from src.main import logger

def get_view_model() -> NavBarViewModel:
    """
    Resetting the nav items active state, load the current_user
    """
    logger.info('\ncurrent_user inside NavBar component:', current_user.get_id())

    return NavBarViewModel(
        nav_items=[
            NavItem(href='/', title='Home', icon=NavItemIcon(original='icons/outline/grid-outline.svg')),
            NavItem(href='/projects', title='Projects', icon=NavItemIcon(original='icons/outline/file-tray-stacked-outline.svg')),
            NavItem(href='/projects', title='Organizations', icon=NavItemIcon(original='icons/outline/business-outline.svg')),
            NavItem(href='/projects', title='Calendar', icon=NavItemIcon(original='icons/outline/calendar-outline.svg')),
        ],
    )


def header_component():
    def component():
        # getting a new view model instance
        vm = get_view_model()

        # getting current requesting path
        req_path = request.path
        print('req path:', req_path)

        # setting the current active page
        vm.set_active_nav_item(path=req_path)
        
        return render_template("components/user/header.html", vm=vm)

    return dict(HeaderComponent=component)
