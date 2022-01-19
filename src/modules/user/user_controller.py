from flask import Blueprint, redirect, url_for, request, flash
from flask.templating import render_template
from src.base.constants.base_constanst import FlashCategory

from src.main import db, admin_permission, manager_permission
from src.modules.user.user_model import User


# defining controller
user = Blueprint('user', __name__, template_folder='templates', static_folder='static', static_url_path='user/static')


@user.route('', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def list():
    users = db.session.query(User).filter(User.activated == True).order_by(User.role_id.asc()).all()
    return render_template("users.html", users=users, title='Tài khoản đang hoạt động')



@user.route('/disabled', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def disabled():
    users = db.session.query(User).filter(User.activated == False).order_by(User.created_time.desc()).all()
    return render_template("users.html", users=users, title='Tài khoản đã khóa')



@user.route('/waiting', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def accounts_waiting():
    users = db.session.query(User).filter(User.activated == False, User.verified_time == None, User.role_id == 3).order_by(User.created_time.desc()).all()
    return render_template("users.html", users=users, title='Đang chờ xác nhận tài khoản')



@user.route('/<int:id>', methods=['GET'])
@admin_permission.require(http_exception=403)
def detail(id: int):
    the_user = db.session.query(User).filter(User.id == id).first()

    if not the_user:
        flash('The user no longer exists', category=FlashCategory.error(50000))
        return redirect(request.referrer or url_for('user.list'))

    return render_template("profile.html", user=the_user)


@user.route('/delete/<int:id>', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def delete():
    the_user = db.session.query(User).get(User.id == id)

    if not the_user:
        flash('The user no longer exists', category=FlashCategory.error(50000))
        return redirect(request.referrer or url_for('user.list'))
    
    return render_template("users.html", user=the_user)


@user.route('/activate/<int:id>', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def activate():
    the_user = db.session.query(User).get(User.id == id)

    if not the_user:
        flash('The user no longer exists', category=FlashCategory.error(50000))
        return redirect(request.referrer or url_for('user.list'))
    
    return render_template("users.html", user=the_user)


@user.route('/deactivate/<int:id>', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def deactivate():
    the_user = db.session.query(User).get(User.id == id)

    if not the_user:
        flash('The user no longer exists', category=FlashCategory.error(50000))
        return redirect(request.referrer or url_for('user.list'))
    
    return render_template("users.html", user=the_user)
