from flask import url_for

from src.base.components.sidebar.sidebar_viewmodel import NavItem, NavItemGroup, NavItemIcon
from src.main import db, db_session

from src.modules.admission.admission_model import Admission, AdmissionPresenter, StudentPresenter
from src.modules.user.user_model import User


def admin_sidebar():
    return [
        NavItemGroup('Chung', items=[
            NavItem(href='/', title='Dashboard', icon=NavItemIcon(original='icons/fluent/outline/apps.svg')),
            # NavItem(href=url_for('home.notifications'), title='Thông báo', icon=NavItemIcon(original='icons/fluent/outline/alert.svg'), counter=5, show_counter_icon=True),
        ],),

        NavItemGroup(label='Tuyển sinh', items=[
            NavItem(href=url_for('admission.list'), title='Các gói tuyển sinh',
                icon=NavItemIcon(original='icons/fluent/outline/hat_graduation.svg'),
                show_counter_icon=True,
                counter=len(db_session.query(Admission).all()),
            ),
        ],),

        NavItemGroup(label='Đại sứ', items=[
            NavItem(href=url_for('admission.waiting'), title='Chờ xét duyệt',
                icon=NavItemIcon(original='icons/fluent/outline/history.svg'),
                counter=len(db_session.query(AdmissionPresenter).filter(AdmissionPresenter.user_joined_time == None).all()),
                show_counter_icon=True,
                counter_is_urgent=True,
            ),
            NavItem(href=url_for('admission.students'), title='Danh sách Học viên',
                icon=NavItemIcon(original='icons/fluent/outline/people_community.svg'),
                show_counter_icon=True,
                counter=len(db_session.query(StudentPresenter).all()),
            ),
        ],),

        NavItemGroup(label='Người dùng', items=[
            NavItem(href=url_for('user.accounts_waiting'), title='Chờ xác thực',
                icon=NavItemIcon(original='icons/fluent/outline/person_question_mark.svg'),
                counter=len(db_session.query(User).filter(User.activated == False, User.verified_time == None, User.role_id == 3).all()),
                show_counter_icon=True,
                counter_is_urgent=True,
            ),
            NavItem(href=url_for('user.list'), title='Đang hoạt động',
                icon=NavItemIcon(original='icons/fluent/outline/person_available.svg'),
                counter=len(db_session.query(User).filter(User.activated == True, ).all()),
            ),
            NavItem(href=url_for('user.disabled'), title='Tài khoản đã khóa',
                icon=NavItemIcon(original='icons/fluent/outline/person_prohibited.svg'),
                counter=len(db_session.query(User).filter(User.activated == False, User.verified_time != None).all()),
                show_counter_icon=True,
            ),
        ],),
        
        NavItemGroup(label='Thiết lập', items=[
            NavItem(href='', title='Mẫu email SMTP', icon=NavItemIcon(original='icons/fluent/outline/mail_template.svg')),
            NavItem(href='', title='Thông tin trang web', icon=NavItemIcon(original='icons/fluent/outline/info.svg')),
        ],),
    ]
