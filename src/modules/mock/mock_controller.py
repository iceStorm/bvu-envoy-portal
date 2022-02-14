from datetime import datetime
from typing import Union
import re
from flask import Blueprint, jsonify, request, render_template, flash, current_app, url_for, make_response, session
from flask_login import login_required, current_user, logout_user, login_user
from werkzeug.utils import redirect

from src.base.constants.base_constanst import FlashCategory
from src.modules.admission.admission_model import AdmissionPresenter, StudentPresenter
from src.main import limiter, db_session

# defining controller
mock = Blueprint('mock', __name__, template_folder='templates', static_folder='static', static_url_path='mock/static')


@mock.route('/student-apply', methods=['GET', 'POST'], defaults={'referral_code': None})
@mock.route('/student-apply/<referral_code>', methods=['GET', 'POST'])
@limiter.limit('1/second; 100/day')
def student_apply(referral_code: Union[str, None]):
    from src.modules.mock.forms.student_apply_form import StudentApplyForm
    form = StudentApplyForm()

    if request.method == 'GET':
        if referral_code:
            presenter = db_session.query(AdmissionPresenter).filter(AdmissionPresenter.referral_code == referral_code).first()
            if presenter != None:
                form.referral_code.data = presenter.referral_code
        return render_template('apply.html', form=form)

    if not form.validate_on_submit():
        flash(message='Please ensure all fields are valid', category=FlashCategory.warning())
        return render_template('apply.html', form=form)

    presenter = db_session.query(AdmissionPresenter).filter(AdmissionPresenter.referral_code == form.referral_code.data).first()
    if presenter == None:
        flash('Referral code invalid')
        return render_template('apply.html', form=form)

    if db_session.query(StudentPresenter).filter(
        StudentPresenter.presenter_id == presenter.id, 
        StudentPresenter.student_id == form.student_id.data
    ).first() != None:
        flash('Already applied to this presenter', category=FlashCategory.error())
        return render_template('apply.html', form=form)

    student = StudentPresenter()
    student.presenter_id = presenter.id
    student.student_id = form.student_id.data
    student.student_joined_time = datetime.now()
    db_session.add(student)
    db_session.commit()

    flash(f'Applied to {presenter.user.full_name} ({ presenter.user.email })', category=FlashCategory.success())
    return render_template('apply.html', form=form)


@mock.route('/student-change-state', methods=['POST'])
@limiter.limit('1/second; 100/day')
def student_paid():
    return jsonify({
        'status': 'not implemented',
    }), 501
