from typing import Mapping

from flask import render_template, redirect, url_for, request, jsonify, json
from flask_login import login_required, current_user
from flask_babel import _
from celery.result import AsyncResult

from web import app, db, celery
from web.models import Task, TaskSetting, TaskStatus
from web.tasks.forms import TaskForm
from web.functions import run_scan


@app.route('/task')
@login_required
def tasks():
    return render_template(
        'tasks/task_list.html',
        tasks=current_user.tasks.order_by('name')
    )


@app.route('/task/create', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    if not form.validate_on_submit():
        return render_template(
            'tasks/edit_task.html',
            form=form,
            action=_('Create task'),
            profiles=json.dumps([
                dict(id=item.id, name=item.name)
                for item in current_user.scan_profiles
            ]),
        )

    task = Task(
        name=form.name.data,
        owner_id=current_user.id
    )
    for item in form.settings:
        task.settings.append(TaskSetting(
            hostname=item.hostname.data,
            profile=item.profile.data,
        ))

    db.session.add(task)
    db.session.commit()

    return redirect(url_for('tasks'))


@app.route('/task/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    if not task_id:
        return redirect(url_for('tasks'))

    task = Task.query.get(task_id)

    if not task:
        return redirect(url_for('tasks'))

    form = TaskForm()

    if not form.validate_on_submit():
        form.populate(task)
        return render_template(
            'tasks/edit_task.html',
            form=form,
            profiles=json.dumps([
                dict(id=item.id, name=item.name)
                for item in current_user.scan_profiles
            ]),
            action=_('Edit task')
        )

    task.name = form.name.data
    all_settings = {
        (item.hostname, item.profile_id): item for item in task.settings
    }

    for item in form.settings:
        if (item.hostname.data, item.profile.data.id) in all_settings:
            continue

        task.settings.append(TaskSetting(
            hostname=item.hostname.data,
            profile=item.profile.data,
        ))

    for item in form.settings:
        all_settings.pop((item.hostname.data, item.profile.data.id), None)

    for item in all_settings.values():
        db.session.delete(item)

    db.session.commit()

    return redirect(url_for('tasks'))


@app.route('/task/delete', methods=['POST'])
@login_required
def delete_tasks():
    tasks = request.form.getlist('tasks_ids[]')
    if not tasks:
        return redirect(url_for('tasks'))

    current_user.tasks.filter(
        Task.id.in_(tasks)
    ).delete(synchronize_session=False)
    db.session.commit()
    return redirect(url_for('tasks'))


@app.route('/task/execute/<int:task_id>', methods=['GET', 'PUT'])
@login_required
def task_execute(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify(dict(error='Wrong task_id')), 404

    if request.method == 'GET':
        result = {}
        if task.status == TaskStatus.Running:
            result = task.uid and AsyncResult(task.uid, app=celery)
            if not result or result.info is None:
                result = {}
            elif not isinstance(result.info, Mapping):
                result = getattr(result.info, 'args', {})
            else:
                result = result.info

        return jsonify(dict(
            task_id=task.id,
            status=task.status.name,
            progress=result
        ))
    data = request.get_json()

    status = data.get('status')
    if not status:
        return jsonify(dict(error='Argument "status" is required')), 400

    try:
        new_status = TaskStatus[status]
    except KeyError:
        return (
            jsonify(dict(
                error=f'Argument "status" might have value '
                      f'only {[item.name for item in TaskStatus]}')),
            400
        )

    task.update_status(new_status)

    if task.status == TaskStatus.Wait and task.uid is None:
        run_scan.apply_async(
            (task.id, current_user.id),
            ignore_result=True,
            countdown=1
        )

    db.session.commit()

    return jsonify(dict(result='ok'))
