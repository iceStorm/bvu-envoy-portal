from flask import Blueprint
from flask.templating import render_template

from src.main import admin_permission, manager_permission

# defining controller
admission = Blueprint('admission', __name__, template_folder='templates', static_folder='static', static_url_path='admission/static')


@admission.route('/add', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def add():
  return render_template("add.html")
