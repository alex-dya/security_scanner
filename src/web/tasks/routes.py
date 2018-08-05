import json

from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user

from web import app, db
from web.models import Task, TaskSetting
from web.tasks.forms import TaskForm


@app.route('/tasks')
@login_required
def tasks():
    return render_template(
        'tasks/task_list.html',
        tasks=current_user.tasks
    )


@app.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    if not form.validate_on_submit():
        return render_template(
            'tasks/edit_task.html',
            form=form,
            action='Create',
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


@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
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
            action='Edit'
        )

    task.name = form.name.data
    all_settings = {
        (item.hostname, item.profile_id): item
        for item in task.settings
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


@app.route('/delete_tasks', methods=['POST'])
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
