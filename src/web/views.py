from flask import render_template, url_for, redirect, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from test_ssh import scan
from web import app, forms, db, login_manager
from web.forms import RegistrationForm, LoginForm
from web.models import User, AccountCredential, ScanProfile


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('main_interface.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    next_page = request.args.get('next')

    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index')

    if current_user.is_authenticated:
        return redirect(next_page)

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        return redirect(next_page)

    return render_template('login.html', form=form, next=next_page)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/run_scan', methods=['GET', 'POST'])
@login_required
def run_scan():
    form = forms.StartTaskForm()
    result = None
    if form.validate_on_submit():
        config = dict(
            unix=dict(
                login=form.username.data,
                password=form.password.data,
                address=form.hostname.data,
                port=form.port.data,
                root_logon=form.root_logon.data,
                root_password=form.root_password.data
            )
        )
        result = scan(config=config)

    return render_template('run_scan.html', form=form, result_list=result)


@app.route('/credentials')
@login_required
def credentials():
    return render_template(
        'credentials.html',
        credential_list=current_user.credentials
    )


@app.route('/create_credential', methods=['GET', 'POST'])
@login_required
def create_credential():
    form = forms.EditCredentialForm()

    if not form.validate_on_submit():
        return render_template(
            'edit_credential.html',
            form=form,
            action='Create'
        )

    cred = AccountCredential(
        username=form.username.data,
        password=form.password.data,
        owner_id=current_user.get_id()
    )
    db.session.add(cred)
    db.session.commit()
    flash(message='New account credential was created')
    return redirect(url_for('credentials'))


@app.route('/edit_credential/<int:cred_id>', methods=['GET', 'POST'])
@login_required
def edit_credential(cred_id):
    if not cred_id:
        return redirect(url_for('credentials'))

    form = forms.EditCredentialForm()
    cred = AccountCredential.query.filter_by(id=cred_id).first()

    if not cred:
        flash('The credential id does not exist')
        return redirect(url_for('credentials'))

    if not form.validate_on_submit():
        form.username.data = cred.username
        form.id.data = cred_id
        form.submit.label.text = 'Edit'

        return render_template(
            'edit_credential.html',
            form=form,
            action='Edit'
        )

    cred.username = form.username.data
    cred.password = form.password.data
    db.session.commit()
    return redirect(url_for('credentials'))


@app.route('/delete_credential', methods=['POST'])
@login_required
def delete_credential():
    creds = request.form.getlist('cred_ids[]')
    if not creds:
        return redirect(url_for('credentials'))

    AccountCredential.query.filter_by(
        owner_id=current_user.get_id()
    ).filter(AccountCredential.id.in_(creds)).delete(synchronize_session=False)
    db.session.commit()
    return redirect(url_for('credentials'))


@app.route('/scan_profiles')
@login_required
def scan_profiles():
    return render_template(
        'scan_profiles.html',
        scan_profiles=current_user.scan_profiles
    )


@app.route('/create_scan_profile', methods=['GET', 'POST'])
@login_required
def create_scan_profile():
    form = forms.ScanProfileForm()

    if not form.validate_on_submit():
        return render_template(
            'edit_profile.html',
            form=form,
            action='Create',
        )

    profile = ScanProfile(
        owner_id=current_user.get_id()
    )
    form.populate_obj(profile)
    db.session.add(profile)
    db.session.commit()
    flash(message='Profile was created')
    return redirect(url_for('scan_profiles'))


@app.route('/edit_scan_profile/<int:profile_id>', methods=['GET', 'POST'])
@login_required
def edit_scan_profile(profile_id):
    profile = current_user.scan_profiles.filter_by(id=profile_id).first()

    if not profile:
        return redirect(url_for('scan_profiles'))

    form = forms.ScanProfileForm()

    if not form.validate_on_submit():
        form.populate(profile)
        return render_template(
            'edit_profile.html',
            form=form,
            action='Edit',
        )

    form.populate_obj(profile)

    db.session.commit()
    flash(message='Profile was edited')
    return redirect(url_for('scan_profiles'))


@app.route('/delete_scan_profile', methods=['POST'])
@login_required
def delete_scan_profile():
    profiles = request.form.getlist('profile_ids[]')
    if not profiles:
        return redirect(url_for('scan_profiles'))

    current_user.scan_profiles.filter(
        ScanProfile.id.in_(profiles)
    ).delete(synchronize_session=False)
    db.session.commit()
    return redirect(url_for('scan_profiles'))


@login_manager.unauthorized_handler
def unathorized_user():
    return_url = url_for('index')
    app.logger.debug(f'request.path: {request.path}')

    if request.path:
        parsed_url = url_parse(request.path)
        return_url = ''.join(parsed_url[2:])
    return redirect(url_for('login', next=return_url))
