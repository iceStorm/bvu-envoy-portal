import datetime

from flask import Blueprint, request, redirect, jsonify
from flask.helpers import flash, url_for
from flask.templating import render_template
from flask_login import current_user

from src.main import admin_permission, manager_permission, db, envoy_permission, db_session
from src.base.constants.base_constanst import FlashCategory
from src.base.decorators.query_params import query_params
from src.modules.admission.admission_model import Admission, AdmissionPresenter
from src.modules.admission.admission_service import AdmissionService
from src.modules.user.user_model import User

# defining controller
admission = Blueprint('admission', __name__, template_folder='templates', static_folder='static', static_url_path='admission/static')


@admission.route('')
@envoy_permission.require(http_exception=403)
@query_params
def list(type=0, page=1, max_per_page=10, start_date=None, end_date=None, status=-1):
    from .forms.admission_filter_form import AdmissionFilterForm
    form = AdmissionFilterForm()
    
    # checking request param data types
    try:
        if start_date:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    except Exception as e:
        flash('Filter value invalid', category=FlashCategory.error())
        return redirect(request.referrer or url_for('admission.list'))
    
    # request param types passed
    form.type.process_data(type)
    form.start_date.process_data(start_date)
    form.end_date.process_data(end_date)
    form.max_per_page.process_data(max_per_page)
    form.status.process_data(status)

    query = db_session.query(Admission)
    print('\ntype:', type, 'per_page:', max_per_page)

    # ignore admissions that current envoy user joined
    if current_user.role.code == 'envoy':
        query = query.join(AdmissionPresenter, AdmissionPresenter.admission_id == Admission.id, isouter=True)
        query = query.filter(AdmissionPresenter.user_id == None)

    # 1. only filter types if the type is not 0
    # 2. only start_date or end_date provided --> find exact
    # 3. both start_date and end_date are provided --> find between

    if type != '0' and type != 0:
        print(type, type != 0)
        query = query.filter(Admission.type_id == type)
  
    if start_date:
        query = query.filter(Admission.start_date == start_date) if not end_date \
            else query.filter(Admission.start_date >= start_date)

    if end_date:
        query = query.filter(Admission.end_date == end_date) if not start_date\
            else query.filter(Admission.end_date <= end_date)
    
    if status != '-1' and status != -1:
        query = query.filter(Admission.finished == (bool(int(status))))

    print(query.as_scalar())
    pagination = query.order_by(Admission.start_date.desc()).paginate(page=int(page or 1), max_per_page=int(max_per_page or 3), error_out=False)
    return render_template("admissions.html", filter_form=form, admissions=pagination)



@admission.route('/waiting')
@envoy_permission.require(http_exception=403)
@query_params
def waiting(page=1, max_per_page=10):
    query = db_session.query(AdmissionPresenter).filter(AdmissionPresenter.user_joined_time == None)
    pagination = query.paginate(page=int(page or 1), max_per_page=int(max_per_page or 3), error_out=False)
    print(pagination.items)
    return render_template("waiting.html", presenters=pagination)



@admission.route('/<int:id>', methods=['GET', 'POST'])
@envoy_permission.require(http_exception=403)
def detail(id):
    the_admission = db_session.query(Admission).filter(Admission.id == id).first()

    if not the_admission:
        flash('The admission no longer exists', category=FlashCategory.error())
        return redirect(request.referrer or url_for('admission.list'))

    # admission found
    return render_template("detail.html", admission=the_admission)



@admission.route('/add', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def add():
    from .forms.admission_form import AdmissionForm
    form = AdmissionForm()

    if request.method == 'GET':
        return render_template("add.html", form=form)

    if not form.validate_on_submit():
        flash(message='Please ensure all fields are valid', category=FlashCategory.warning())
        return render_template("add.html", form=form)

    new_addmission = Admission(
        name=form.name.data,
        description=form.description.data,
        start_date=form.start_date.data,
        end_date=form.end_date.data,
        type_id=form.type.data,
        rose=form.rose.data,
    )
    if not AdmissionService.add(new_addmission):
        flash(message='Error occur when adding Admission', category=FlashCategory.error())
        return render_template("add.html", form=form)

    flash(message='Added', category=FlashCategory.success())
    return redirect(request.referrer or url_for('admission.list'))



@admission.route('/edit/<int:id>', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def edit(id: int):
    the_admission = db_session.query(Admission).filter(Admission.id == id).first()

    if not the_admission:
        flash('The admission no longer exists', category=FlashCategory.error())
        return redirect(request.referrer or url_for('admission.list'))


    from .forms.admission_form import AdmissionForm
    form = AdmissionForm()
    form._model = the_admission

    if request.method == 'GET':
        # assigning existing admission data
        form.type.process_data(the_admission.type_id)
        form.name.process_data(the_admission.name)
        form.start_date.process_data(the_admission.start_date)
        form.end_date.process_data(the_admission.end_date)
        form.description.process_data(the_admission.description)
        form.rose.process_data(the_admission.rose)
        # form.slug.process_data(admission.slug)
        return render_template("add.html", form=form, editing=True)

    if not form.validate_on_submit():
        flash(message='Please ensure all fields are valid', category=FlashCategory.warning())
        return render_template("add.html", form=form)

    if not AdmissionService.update(the_admission, form):
        flash(message='Error occur when updating Admission', category=FlashCategory.error())
        return render_template("add.html", form=form)

    flash(message='Updated', category=FlashCategory.success())
    return redirect(request.referrer or url_for('admission.list'))



@admission.route('/delete/<int:id>', methods=['GET'])
@admin_permission.require(http_exception=403)
def delete(id: int):
    the_admission = db_session.query(Admission).filter(Admission.id == id).first()

    if not the_admission:
        flash('The admission no longer exists', category=FlashCategory.error())
        return redirect(url_for('admission.delete'))

    if not AdmissionService.delete(the_admission):
        flash(message='Error occur when adding Admission', category=FlashCategory.error())
        return redirect(url_for('admission.delete'))

    flash(message='Removed', category=FlashCategory.success())
    return redirect(request.referrer or url_for('admission.list'))



@admission.route('/mark_done/<int:id>', methods=['GET'])
@admin_permission.require(http_exception=403)
def mark_done(id: int):
    admission = db_session.query(Admission).filter(Admission.id == id).first()

    if not admission:
        flash('The admission no longer exists', category=FlashCategory.error())
        return redirect(request.referrer or url_for('admission.list'))

    # check if the end_date is met:
    if not admission.end_date == datetime.datetime.today().date():
        flash(message='End date not met. Please wait until the end date is met, or modify the end date to today.', category=FlashCategory.error())
        return redirect(request.referrer or url_for('admission.list'))

    if not AdmissionService.mark_done(admission):
        flash(message='Error occur when marking done the Admission', category=FlashCategory.error())
        return redirect(request.referrer or url_for('admission.list'))

    flash(message='Finished', category=FlashCategory.success())
    return redirect(request.referrer or url_for('admission.list'))



@admission.route('/revoke_done/<int:id>', methods=['GET'])
@admin_permission.require(http_exception=403)
def revoke_done(id: int):
    admission = db_session.query(Admission).filter(Admission.id == id).first()

    if not admission:
        flash('The admission no longer exists', category=FlashCategory.error())
        return redirect(request.referrer or url_for('admission.list'))

    if not AdmissionService.mark_done(admission, revoke=True):
        flash(message='Error occur when revoking done the Admission', category=FlashCategory.error())
        return redirect(request.referrer or url_for('admission.list'))

    flash(message='Revoked', category=FlashCategory.success())
    return redirect(request.referrer or url_for('admission.list'))



@admission.route('envoy-apply/<int:id>', methods=['GET'])
@envoy_permission.require(http_exception=403)
def envoy_register(id: int):
    admission = db_session.query(Admission).filter(Admission.id == id).first()

    if not admission:
        flash('The admission no longer exists', category=FlashCategory.error())
        return redirect(request.referrer or url_for('admission.list'))
    
    if not AdmissionService.envoy_apply(envoy_id=current_user.id, admission_id=id):
        flash('Error applying to the admission', category=FlashCategory.error())
        return redirect(request.referrer or url_for('admission.list'))
    
    flash('Requested, please wait for admin approval', category=FlashCategory.success())
    return redirect(request.referrer or url_for('admission.list'))


@admission.route('approve-envoy/<int:envoy_id>/<int:admission_id>', methods=['GET'])
@admin_permission.require(http_exception=403)
def approve_envoy(admission_id: int, envoy_id: int):
    print(admission_id, envoy_id)

    presenter = db_session.query(AdmissionPresenter).filter(
        AdmissionPresenter.user_id == envoy_id,
        AdmissionPresenter.admission_id == admission_id,
    ).first()

    print(presenter)
    if presenter == None:
        flash('The presenter no longer exists', category=FlashCategory.error())
        return redirect(request.referrer or url_for('admission.list'))
    
    presenter.user_joined_time = datetime.datetime.now()
    db_session.commit()

    flash('Approved', category=FlashCategory.success())
    return redirect(request.referrer or url_for('admission.list'))



@admission.route('unapprove-envoy/<int:envoy_id>/<int:admission_id>', methods=['GET'])
@admin_permission.require(http_exception=403)
def unapprove_envoy(envoy_id: int, admission_id: int):
    presenter = db_session.query(AdmissionPresenter).filter(
        AdmissionPresenter.user_id == envoy_id,
        AdmissionPresenter.admission_id == admission_id,
    ).first()

    if presenter == None:
        flash('The presenter no longer exists', category=FlashCategory.error())
        return redirect(request.referrer or url_for('admission.list'))
    
    db_session.delete(presenter)
    db_session.commit()

    flash('Declined', category=FlashCategory.error())
    return redirect(request.referrer or url_for('admission.list'))



@admission.route('envoy-leave/<int:id>', methods=['GET'])
@envoy_permission.require(http_exception=403)
def envoy_leave(id: int):
    presenter = db_session.query(AdmissionPresenter).filter(
        AdmissionPresenter.user_id == current_user.id,
        AdmissionPresenter.admission_id == id,
    ).first()

    if not presenter:
        flash('The admission no longer exists', category=FlashCategory.error())
        return redirect(request.referrer or url_for('admission.list'))
    
    if not AdmissionService.envoy_leave(presenter=presenter):
        flash('Error leaving the admission', category=FlashCategory.error())
        return redirect(request.referrer or url_for('admission.list'))
    
    flash('Left', category=FlashCategory.success())
    return redirect(request.referrer or url_for('admission.list'))


@admission.route('student-apply', methods=['POST'])
def student_apply():
    return jsonify({
        'status': 'not implemented',
    }), 501


@admission.route('student-change-state', methods=['POST'])
def student_change_state():
    return jsonify({
        'status': 'not implemented',
    }), 501
