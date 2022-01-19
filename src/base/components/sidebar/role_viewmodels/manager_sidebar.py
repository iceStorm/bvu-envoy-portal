from flask import url_for

from src.base.components.sidebar.sidebar_viewmodel import NavItem, NavItemGroup, NavItemIcon
from src.main import db

from src.modules.admission.admission_model import Admission
from src.modules.user.user_model import User


def manager_sidebar():
    return [
        NavItemGroup('Chung', items=[
            NavItem(href='/', title='Dashboard', icon=NavItemIcon(original='icons/fluent/outline/apps.svg')),
            NavItem(href=url_for('home.notifications'), title='Thông báo', icon=NavItemIcon(original='icons/fluent/outline/alert.svg'), counter=5, show_counter_icon=True),
        ],),

        NavItemGroup(label='Tuyển sinh', items=[
            NavItem(href=url_for('admission.list'), title='Các gói tuyển sinh',
                icon=NavItemIcon(original='icons/fluent/outline/hat_graduation.svg'),
                show_counter_icon=True,
                counter=len(db.session.query(Admission).all()),
            ),
        ],),

        NavItemGroup(label='Đại sứ - Học viên', items=[
            NavItem(href='', title='Chờ xét duyệt',
                icon=NavItemIcon(original='icons/fluent/outline/history.svg'),
                counter=len(db.session.query(User).filter(User.activated == False, User.role_id == 3).all()),
                show_counter_icon=True,
            ),
            NavItem(href='', title='Danh sách Đại sứ',
                icon=NavItemIcon(original='icons/fluent/outline/people_team.svg'),
                show_counter_icon=True,
                counter=len(db.session.query(User).filter(User.role_id == 3, User.activated == True).all()),
            ),
            NavItem(href='', title='Danh sách Học viên',
                icon=NavItemIcon(original='icons/fluent/outline/people_community.svg'),
                show_counter_icon=True,
                counter=len(db.session.query(User).filter(User.role_id == 3, User.activated == True).all()),
            ),
        ],),
    ]
