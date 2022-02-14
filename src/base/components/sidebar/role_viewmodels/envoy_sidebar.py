import datetime
from flask import url_for
from flask_login import current_user

from src.base.components.sidebar.sidebar_viewmodel import NavItem, NavItemGroup, NavItemIcon
from src.main import db_session

from src.modules.admission.admission_model import Admission, AdmissionPresenter
from src.modules.user.user_model import User


def envoy_sidebar():
    return [
        NavItemGroup('Chung', items=[
            NavItem(href='/', title='Dashboard', icon=NavItemIcon(original='icons/fluent/outline/apps.svg')),
            NavItem(href=url_for('home.notifications'), title='Thông báo', icon=NavItemIcon(original='icons/fluent/outline/alert.svg'), counter=5, show_counter_icon=True),
        ],),

        NavItemGroup(label='Tuyển sinh', items=[
            NavItem(href=url_for('admission.list'), title='Các gói tuyển sinh',
                icon=NavItemIcon(original='icons/fluent/outline/hat_graduation.svg'),
                show_counter_icon=True,
                counter=len(db_session.query(Admission).filter(
                    Admission.finished == False,
                    # Admission.end_date >= datetime.datetime.today()
                ).all()),
            ),
        ],),

        NavItemGroup(label='Đại sứ - Học viên', items=[
            NavItem(href='', title='Chờ xét duyệt',
                icon=NavItemIcon(original='icons/fluent/outline/history.svg'),
                counter=len(db_session.query(User).filter(User.activated == False, User.role_id == 3).all()),
                show_counter_icon=True,
            ),
            NavItem(href=url_for('admission.list'), title='Chiến dịch đã tham gia',
                icon=NavItemIcon(original='icons/fluent/outline/hat_graduation.svg'),
                show_counter_icon=True,
                counter=len(db_session.query(AdmissionPresenter).filter(
                    AdmissionPresenter.user_id == current_user.id,
                    AdmissionPresenter.user_joined_time != None,
                ).all()),
            ),
            NavItem(href='', title='Danh sách Học viên',
                icon=NavItemIcon(original='icons/fluent/outline/people_community.svg'),
                show_counter_icon=True,
                counter=len(db_session.query(User).filter(User.role_id == 3, User.activated == True).all()),
            ),
        ],),
    ]
