from flask import Blueprint
from flask.templating import render_template

from src.main import admin_permission, manager_permission

# defining controller
user = Blueprint('user', __name__, template_folder='templates', static_folder='static', static_url_path='user/static')


@user.route('/list', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def list():
    return render_template("users.html")
