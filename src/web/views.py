from flask import render_template, url_for, redirect, request

from web import app, forms
from test_ssh import scan


@app.route('/')
@app.route('/index')
def index():
    title = app.config.get('TITLE')
    return render_template('main_interface.html',
                           title=title)


@app.route('/run_scan', methods=['GET', 'POST'])
def run_scan():
    form = forms.StartTaskForm()
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
        return render_template('run_scan.html', title='TITLE', form=form, result_list=result)
    return render_template('run_scan.html', title='TITLE', form=form)
