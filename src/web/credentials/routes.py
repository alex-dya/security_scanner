from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from flask_babel import _

from web.credentials import forms
from web import app, db
from web.models import AccountCredential


ACTIVE = 'credentials'


@app.route('/credentials')
@login_required
def credentials():
    return render_template(
        'credentials/credential_list.html',
        credential_list=current_user.credentials,
        active=ACTIVE,
    )


@app.route('/credentials/create', methods=['GET', 'POST'])
@login_required
def create_credential():
    form = forms.EditCredentialForm()

    if not form.validate_on_submit():
        return render_template(
            'credentials/edit_credential.html',
            form=form,
            action=_('Create credential'),
            active=ACTIVE,
        )

    cred = AccountCredential(
        name=form.name.data,
        username=form.username.data,
        password=form.password.data,
        owner_id=current_user.get_id()
    )

    db.session.add(cred)
    db.session.commit()
    flash(_('New account credential was created'))
    return redirect(url_for('credentials'))


@app.route('/credentials/edit/<int:cred_id>', methods=['GET', 'POST'])
@login_required
def edit_credential(cred_id):
    if not cred_id:
        return redirect(url_for('credentials'))

    form = forms.EditCredentialForm()
    cred = AccountCredential.query.filter_by(id=cred_id).first()

    if not cred:
        flash(_('The credential id does not exist'))
        return redirect(url_for('credentials'))

    if not form.validate_on_submit():
        form.name.data = cred.name
        form.username.data = cred.username
        form.id.data = cred_id

        return render_template(
            'credentials/edit_credential.html',
            form=form,
            action=_('Edit credential'),
            active=ACTIVE,
        )

    cred.name = form.name.data
    cred.username = form.username.data
    cred.password = form.password.data
    db.session.commit()
    return redirect(url_for('credentials'))


@app.route('/credentials/delete', methods=['POST'])
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
