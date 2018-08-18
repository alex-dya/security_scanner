from time import sleep

from flask import json

from scanner import transports, controls
from scanner.detect import detect
from web import celery, models, db, app


def prepare_task(self, task_id, owner_id):
    task = models.Task.query.get(task_id)
    task.status = models.TaskStatus.Running
    task.uid = self.request.id
    result = models.TaskResult(task_id=task_id, owner_id=owner_id)
    db.session.add(result)
    db.session.commit()
    return result


def postprocess_task(task_id, result):
    task = models.Task.query.get(task_id)
    task.status = models.TaskStatus.Idle
    task.uid = None
    result.finish()
    db.session.commit()


@celery.task(bind=True)
def summ(self, task_id, owner_id):
    total = 15
    self.update_state(
        state='PROGRESS',
        meta={'current': 0, 'total': total}
    )
    result = prepare_task(self, task_id, owner_id)

    result = 0
    for i in range(total):
        sleep(1)
        result += i
        if not self.request.called_directly:
            app.logger.debug('UPDATE porgress')
            self.update_state(
                state='PROGRESS',
                meta={'current': i+1, 'total': total}
            )

    postprocess_task(task_id, result)


@celery.task(bind=True)
def run_scan(self, task_id, owner_id):
    total = len(list(controls.iter_controls()))
    self.update_state(
        state='PROGRESS',
        meta={'current': 0, 'total': total}
    )
    result = prepare_task(self, task_id, owner_id)
    task = models.Task.query.get(task_id)
    for setting in task.settings:
        host_result = models.HostResult(
            task_id=result.id,
            hostname=setting.hostname,
            config=json.dumps(setting.profile.to_dict())
        )
        result.host_results.append(host_result)
        config = dict(
            hostname=setting.hostname,
            **setting.profile.to_dict()
        )
        app.logger.debug(f'Config: {config}')
        transports.config = config
        detect()
        for idx, control in enumerate(controls.iter_controls(), 1):
            control.run()
            self.update_state(
                state='PROGRESS',
                meta={'current': idx, 'total': total}
            )

        controls_is_getting = set()
        for control in controls.iter_controls():
            if control.control.number in controls_is_getting:
                continue

            controls_is_getting.add(control.control.number)
            control_result = models.ControlResult(
                control_number=control.control.number,
                status=control.control.status,
                result=control.result
            )
            host_result.controls.append(control_result)

        transports.reset_transports()

    postprocess_task(task_id, result)
