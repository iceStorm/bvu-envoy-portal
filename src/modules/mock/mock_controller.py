from flask import Blueprint, jsonify, request, render_template, flash, current_app, url_for, make_response, session
from flask_login import login_required, current_user, logout_user, login_user
from werkzeug.utils import redirect

# defining controller
mock = Blueprint('mock', __name__, template_folder='templates', static_folder='static', static_url_path='mock/static')


@mock.route('/apply', methods=['GET', 'POST'])
def apply():
    return render_template('apply.html')
