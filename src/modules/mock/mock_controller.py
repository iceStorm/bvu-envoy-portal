from datetime import datetime
from typing import Union
import re
from flask import Blueprint, jsonify, request, render_template, flash, current_app, url_for, make_response, session
from flask_login import login_required, current_user, logout_user, login_user
from werkzeug.utils import redirect

from src.base.constants.base_constanst import FlashCategory
from src.modules.admission.admission_model import AdmissionPresenter, StudentPresenter
from src.main import limiter, db_session, admin_permission

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

    # referral codes are unique
    presenter = db_session.query(AdmissionPresenter).filter(AdmissionPresenter.referral_code == form.referral_code.data).first()
    if presenter == None:
        flash('Referral code invalid', category=FlashCategory.warning())
        return render_template('apply.html', form=form)

    if presenter.admission.finished or presenter.admission.end_date < datetime.now().date():
        flash('The admission no longer opens', category=FlashCategory.warning())
        return render_template('apply.html', form=form)

    query = db_session.query(StudentPresenter).filter(
        StudentPresenter.presenter_id == presenter.id,
        StudentPresenter.student_id == form.student_id.data,
    )
    print(query)
    if query.first() != None:
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


@mock.route('/edit-student/<int:student_id>/<int:presenter_id>', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def edit_student(student_id: int, presenter_id: int):
    the_student = db_session.query(StudentPresenter).filter(
        StudentPresenter.student_id == student_id,
        StudentPresenter.presenter_id == presenter_id,
    ).first()

    if the_student == None:
        flash('The student no longer exists', category=FlashCategory.warning())
        return redirect(request.referrer or '/')

    from src.modules.mock.forms.student_edit_form import StudentEditForm
    form = StudentEditForm()

    if request.method == 'GET':
        form.referral_code.data = the_student.presenter.referral_code
        form.student_id.data = the_student.student_id
        form.paid_time.data = the_student.student_paid_time
        form.applied_time.data = the_student.student_joined_time
        form.envoy_name.data = the_student.presenter.user.full_name
        form.envoy_contact.data = the_student.presenter.user.email
        return render_template('edit.html', form=form)

    if not form.validate_on_submit():
        flash('Info invalid', category=FlashCategory.warning())
        return render_template('edit.html', form=form)

    print(form.paid_time.data)
    the_student.student_paid_time = form.paid_time.data
    db_session.commit()

    flash('Updated', category=FlashCategory.success())
    return render_template('edit.html', form=form)



@mock.route('/remove-student/<int:student_id>/<int:presenter_id>', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def remove_student(student_id: int, presenter_id: int):
    the_student = db_session.query(StudentPresenter).filter(
        StudentPresenter.student_id == student_id,
        StudentPresenter.presenter_id == presenter_id,
    ).first()

    if the_student == None:
        flash('The student no longer exists', category=FlashCategory.warning())
        return redirect(request.referrer or '/')
    
    db_session.delete(the_student)
    db_session.commit()

    flash('Deleted', category=FlashCategory.success())
    return redirect(request.referrer or '/')
