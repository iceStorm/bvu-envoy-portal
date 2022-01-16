from flask import request, render_template
from flask.helpers import url_for
from flask_login import current_user

from .sidebar_viewmodel import NavBarViewModel, NavItem, NavItemIcon, NavItemGroup

# import this model to handle the DB (Flask-SQLAlchemy)
from src.modules.user.user_model import User
from src.modules.admission.admission_model import Admission
from src.main import logger, db

def get_view_model() -> NavBarViewModel:
    """
    Resetting the nav items active state, load the current_user
    """
    print('\ncurrent_user inside NavBar component:', current_user.id)

    return NavBarViewModel(
        nav_item_groups=[
            NavItemGroup('Chung', items=[
                NavItem(href='/', title='Dashboard', icon=NavItemIcon(original='icons/fluent/outline/apps.svg')),
                NavItem(href=url_for('home.notifications'), title='Thông báo', icon=NavItemIcon(original='icons/fluent/outline/alert.svg'), counter=5, show_counter_icon=True),
            ],),

            NavItemGroup(label='Tuyển sinh', items=[
                NavItem(href=url_for('admission.active'), title='Đang diễn ra', 
                    icon=NavItemIcon(original='icons/fluent/outline/arrow_trending.svg'),
                    show_counter_icon=True,
                    counter=len(Admission.get_available_items_to_new_registration()),
                ),
                NavItem(href=url_for('admission.list'), title='Các gói tuyển sinh',
                    icon=NavItemIcon(original='icons/fluent/outline/hat_graduation.svg'),
                    show_counter_icon=True,
                    counter=len(db.session.query(Admission).all()),
                ),
            ],),

            NavItemGroup(label='Đại sứ', items=[
                NavItem(href='', title='Chờ xét duyệt',
                    icon=NavItemIcon(original='icons/fluent/outline/history.svg'),
                    counter=len(db.session.query(User).filter(User.activated == False, User.role_id == 3).all()),
                    show_counter_icon=True,
                ),
                NavItem(href='', title='Các đại sứ',
                    icon=NavItemIcon(original='icons/fluent/outline/people_swap.svg'),
                    show_counter_icon=True,
                    counter=len(db.session.query(User).filter(User.role_id == 3, User.activated == True).all()),
                ),
            ],),

            NavItemGroup(label='Người dùng', items=[
                NavItem(href=url_for('user.list'), title='Danh sách tài khoản',
                    icon=NavItemIcon(original='icons/fluent/outline/people.svg'),
                    counter=len(db.session.query(User).all()),
                ),
            ],),
            
            NavItemGroup(label='Thiết lập', items=[
                NavItem(href='', title='Mẫu email SMTP', icon=NavItemIcon(original='icons/fluent/outline/mail_template.svg')),
                NavItem(href='', title='Thông tin trang web', icon=NavItemIcon(original='icons/fluent/outline/info.svg')),
            ],),
        ],
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
