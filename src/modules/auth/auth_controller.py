import uuid
from flask import Blueprint, jsonify, request, render_template, flash, current_app, url_for, make_response, session
from flask_login import login_required, current_user, logout_user, login_user
from werkzeug.utils import redirect

from src.main import limiter, logger
from src.base.constants.base_constanst import FlashCategory
from src.modules.auth.auth_service import AuthService
from src.modules.user.user_model import User

# defining controller
auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static', static_url_path='auth/static')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # grabbing the form
    from src.modules.auth.forms.login_form import LoginForm
    form = LoginForm()

    # checking if is GET request
    if request.method == 'GET':
        # redirecting logged-in user to the index page
        if current_user.is_authenticated:
            flash('You\'re already logged in!', category=FlashCategory.warning(5000))
            return redirect('/')

        if request.args.get('email'):
            form.email.data = request.args.get('email')
        return render_template('login.html', form=form)

    # POST REQUEST
    # checking if the form is not valid yet
    if not form.validate_on_submit():
        return render_template('login.html', form=form)

    # FORM IS VALID, LET'S GET THE USER OBJECT FROM DB
    from src.modules.user.user_model import User
    from src.main import db
    user = AuthService.get_user_from_email(form.email.data)
    
    if user is not None:
        # let's log the user in
        login_user(user, remember=form.remember)

        #  Tell Flask-Principal the identity changed
        from flask_principal import identity_changed, Identity
        identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

        # finally, redirect the user to desired page or index page
        next_url = request.args.get('next')
        return redirect(next_url if next_url else '/')
    
    flash(message='The user no longer exists', category=FlashCategory.Error)
    return render_template('login.html', form=form)


@auth.route('/logout', methods=['POST'])
@limiter.limit('5/minute')
@login_required
def logout():
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    from flask_principal import identity_changed, Identity, AnonymousIdentity
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())

    return redirect(location="/")


@auth.route('/register', methods=['GET', 'POST'])
@limiter.limit('1/second; 15/minute; 20/day')
def register():
    # grabbing the form
    from src.modules.auth.forms.signup_form import SignUpForm
    form = SignUpForm()

    # checking if is GET request
    if request.method == 'GET':
        # redirecting logged-in user to the index page
        if current_user.is_authenticated:
            flash('Please logout first, then signup!', category=FlashCategory.warning())
            return redirect('/')
        return render_template('signup.html', form=form)

    # post requests
    # checking if the form is not valid yet
    if not form.validate_on_submit():
        flash('Please ensure all fields have no errors!', category=FlashCategory.warning(7500))
        return render_template('signup.html', form=form)

    try:
        # all validation passed, let's continue handle the signup process
        AuthService.send_register_confirm_email(
            receiver_email=form.email.data,
            receiver_name=form.organization_name.data,
            code=AuthService.gen_registration_code(),
        )

        # showing a flash message -> redirecting to the home page
        flash(message=f'Vui lòng kiểm tra tin nhắn được gửi tới email {form.email.data} để hoàn tất quá trình đăng ký!', category=FlashCategory.success(20000))

        # push the form data to session, so we dont have to store these info in the DB --> prevent registrastion spamming
        session['registration_organization_name'] = form.organization_name.data
        session['registration_organization_representer_person_name'] = form.organization_representer_person_name.data
        session['registration_organization_tax_id'] = form.organization_tax_id.data
        session['registration_citizen_id'] = form.citizen_id.data
        session['registration_email'] = form.email.data
        session['registration_phone'] = form.phone.data
        session['registration_address'] = form.address.data

        # show the verification page
        return redirect('/verify')
    except Exception as e:
        logger.error(e)
        flash(message=f'Có lỗi xảy ra trong quá trình xử lý, vui lòng thử lại sau', category=FlashCategory.error(20000))
        return render_template('signup.html', form=form)


@auth.route('verify', methods=['GET', 'POST'])
@limiter.limit('1/second; 15/minute; 20/day')
def verify_registration():
    # grabbing the form
    from src.modules.auth.forms.verification_form import RegisterVerificationForm
    form = RegisterVerificationForm()

    if session.get('registration_email') is None or session.get('registration_code') is None:
        flash(message='Seemslike you have already registered, please try later', category=FlashCategory.warning(10000))
        return redirect('/')

    if request.method == 'GET':
        return render_template('verify-registration.html', form=form, email=session['registration_email'])

    if not form.validate_on_submit():
        flash(message='Please fill out the code', category=FlashCategory.warning())
        return render_template('verify-registration.html', form=form, email=session['registration_email'])

    # form validated --> check if the provided code is correct
    if form.verification_code.data != session.get('registration_code'):
        flash(message='The code you provided was incorrect', category=FlashCategory.warning())
        return render_template('verify-registration.html', form=form, email=session['registration_email'])

    # form validated -> add the envoy info to DB
    try:
        new_user = User(email=session['registration_email'], phone_number=session['registration_phone'])
        new_user.role_id = 3 # envoy
        new_user.envoy_type_id = 4 # organization
        new_user.address = session['registration_address']
        new_user.citizen_id = session['registration_citizen_id']
        new_user.organization_name  = session['registration_organization_name']
        new_user.organization_representer_person_name = session['registration_organization_representer_person_name']
        new_user.organization_tax_id = session['registration_organization_tax_id']

        # ??? check trùng thông tin trước khi thêm vào DB

        if AuthService.register(new_user=new_user):
            flash(message='Đăng ký tài khoản Đại sứ BVU thành công', category=FlashCategory.success(10000))
            response = make_response(render_template('registration-success.html', email=new_user.email))
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            session.clear()
            return response

        # DB insert error
        flash(message='Something went wrong with your info, please try to register again', category=FlashCategory.warning())
        return render_template('verify-registration.html', form=form, email=session['registration_email'])

    except Exception as e:
        logger.error(e)
        flash(message='Something went wrong, please try later', category=FlashCategory.warning())
        return render_template('verify-registration.html', form=form, email=session['registration_email'])



@auth.route('/reset-password', methods=['POST'])
def reset_password():
    from src.modules.auth.auth_service import AuthService

    AuthService.send_reset_password_email(request.email)
    return "password reset", 200


@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    from src.modules.auth.forms.profile_form import UpdateForm
    form = UpdateForm()

    from src.modules.user.user_model import User
    current_user_object = User.query.get(current_user.get_id())  # type: User

    # assigning current user's email for every requests --- the email field is not editable (primary key)
    form.email.data = current_user_object.email
    print('avatar:', form.avatar)


    # checking if is GET request
    if request.method == 'GET':
        # re-assigning the full_name to latest value
        form.full_name.data = current_user_object.full_name
        return render_template('profile.html', form=form)

    # checking if the form is not valid yet
    if not form.validate_on_submit():
        # re-assigning the full_name to reduce confusing
        form.full_name.data = current_user_object.full_name

        flash('form error !', category='error')
        return render_template('profile.html', form=form)


    # all validations passed, let's update the user's new data
    # saving the new avatar_url to the DB if a avatar choosen
    from src.modules.auth.auth_service import AuthService
    avatar_path = None
    print('image data:', form.avatar.data)
    if form.avatar.data:
        avatar_path = AuthService.save_avatar_image(form.avatar.data)
        print('saved avatar path:', avatar_path)

    try:
        # the avatar field now is not a file (via: request.files)
        if request.form['avatar'] == 'null':
            avatar_path = 'null'
    except:
        print('')

    # updating the user's new data
    user = User(full_name=form.full_name.data, avatar_url=avatar_path)
    AuthService.update(current_user.get_id(), user)


    flash('Updated !', category=FlashCategory.Success)
    return redirect(location='profile')


