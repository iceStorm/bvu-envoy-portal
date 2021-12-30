from flask import Blueprint, render_template, g, current_app, request, jsonify, flash
from flask_login import current_user

# defining controller
# the static_url_path='home/static' means: this route has registered with url_prefix='/' - same as base/static,
# so we need to add an alias name (will be displayed on the Browser's url bar)
# the alias 'home' here to prevent conflicting resource between the main app vs this route
home = Blueprint('index', __name__, template_folder='templates', static_folder='static', static_url_path='home/static')

from src.main import limiter


@home.route("/", methods=["GET"])
@limiter.limit('1/second')
def index():
    return render_template('index.html' if not current_user.is_authenticated else f"index-{current_user.role}")
