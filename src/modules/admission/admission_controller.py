import datetime

from flask import Blueprint, request, redirect
from flask.helpers import flash, url_for
from flask.templating import render_template

from src.main import admin_permission, manager_permission, db
from src.base.constants.base_constanst import FlashCategory
from src.base.decorators.query_params import query_params
from src.modules.admission.admission_model import Admission
from src.modules.admission.admission_service import AdmissionService

# defining controller
admission = Blueprint('admission', __name__, template_folder='templates', static_folder='static', static_url_path='admission/static')


@admission.route('',)
@admin_permission.require(http_exception=403)
@query_params
def list(type=0, page=1, max_per_page=6, start_date=None, end_date=None):
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
        print('referrer:', request.headers.get('HTTP_REFERER', ''))
        return redirect(request.headers.get('HTTP_REFERER', ''))
    
    # request param types passed
    form.type.process_data(type)
    form.start_date.process_data(start_date)
    form.end_date.process_data(end_date)
    form.max_per_page.process_data(max_per_page)

    query = db.session.query(Admission)
    print('\ntype:', type, 'per_page:', max_per_page)

    # 1.
    # only filter types if the type is not 0
    if type != '0' and type != 0:
        print(type, type != 0)
        print('have type...')
        query = query.filter(Admission.type_id == type)

    # 2.
    if start_date:
        print('have start_date...')
        query = query.filter(Admission.start_date == start_date)
        
    # 3.
    # only end_date provided --> find exact
    if end_date:
        # start_date & end_date provided --> find between
        if start_date:
            print('and have end_date...')
            query = query.filter(Admission.end_date <= end_date)
        else:
            print('only end_date...')
            query = query.filter(Admission.end_date == end_date)

    print(query.as_scalar())
    pagination = query.paginate(page=int(page), max_per_page=int(max_per_page), error_out=False)
    print('returning...', pagination.items)
    return render_template("admissions.html", filter_form=form, admissions=pagination)



@admission.route('/active', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def active():
    return render_template("admissions.html")



@admission.route('/<int:id>', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def detail(id):
    admission = db.session.query(Admission).filter(Admission.id == id).first()

    if not admission:
        flash('The admission no longer exists', category=FlashCategory.error())
        return redirect(request.headers.get('HTTP_REFERER', ''))

    # admission found
    return render_template("detail.html", admission=admission)



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
        # slug=form.slug.data,
    )
    if not AdmissionService.add(new_addmission):
        flash(message='Error occur when adding Admission', category=FlashCategory.error())
        return render_template("add.html", form=form)

    flash(message='Added', category=FlashCategory.success())
    return redirect(url_for('admission.list'))



@admission.route('/edit/<int:id>', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def edit(id: int):
    admission = db.session.query(Admission).filter(Admission.id == id).first()

    if not admission:
        flash('The admission no longer exists', category=FlashCategory.error())
        return redirect(request.referrer)


    from .forms.admission_form import AdmissionForm
    form = AdmissionForm()
    form._editing = True

    if request.method == 'GET':
        # assigning existing admission data
        form.type.process_data(admission.type)
        form.name.process_data(admission.name)
        form.start_date.process_data(admission.start_date)
        form.end_date.process_data(admission.end_date)
        form.description.process_data(admission.description)
        # form.slug.process_data(admission.slug)
        return render_template("add.html", form=form, editing=True)

    if not form.validate_on_submit():
        flash(message='Please ensure all fields are valid', category=FlashCategory.warning())
        return render_template("add.html", form=form)

    if not AdmissionService.update(admission, form):
        flash(message='Error occur when updating Admission', category=FlashCategory.error())
        return render_template("add.html", form=form)

    flash(message='Updated', category=FlashCategory.success())
    return redirect(url_for('admission.list'))



@admission.route('/delete/<int:id>', methods=['GET'])
@admin_permission.require(http_exception=403)
def delete(id: int):
    admission = db.session.query(Admission).filter(Admission.id == id).first()

    if not admission:
        flash('The admission no longer exists', category=FlashCategory.error())
        return redirect(request.headers.get('HTTP_REFERER', ''))

    if not AdmissionService.delete(admission):
        flash(message='Error occur when adding Admission', category=FlashCategory.error())
        return redirect(request.headers.get('HTTP_REFERER', ''))

    flash(message='Removed', category=FlashCategory.success())
    return redirect(url_for('admission.list'))



@admission.route('/mark_done/<int:id>', methods=['GET'])
@admin_permission.require(http_exception=403)
def mark_done(id: int):
    admission = db.session.query(Admission).filter(Admission.id == id).first()

    if not admission:
        flash('The admission no longer exists', category=FlashCategory.error())
        return redirect(request.headers.get('HTTP_REFERER', ''))

    if not AdmissionService.delete(admission):
        flash(message='Error occur when adding Admission', category=FlashCategory.error())
        return redirect(request.headers.get('HTTP_REFERER', ''))

    flash(message='Removed', category=FlashCategory.success())
    return redirect(url_for('admission.list'))
