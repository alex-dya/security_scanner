from datetime import datetime
from time import sleep

from web import celery, models, db, app


def prepare_task(self, task_id, owner_id):
    task = models.Task.query.get(task_id)
    task.status = models.TaskStatus.Running
    task.uid = self.request.id
    result = models.TaskResult(task_id=task_id, owner_id=owner_id)
    db.session.add(result)
    db.session.commit()
    return result.id


def postprocess_task(task_id, result_id):
    task = models.Task.query.get(task_id)
    task.status = models.TaskStatus.Idle
    task.uid = None
    result = models.TaskResult.query.get(result_id)
    result.finish()
    db.session.commit()


@celery.task(bind=True)
def summ(self, task_id, owner_id):
    total = 15
    self.update_state(
        state='PROGRESS',
        meta={'current': 0, 'total': total}
    )
    result_id = prepare_task(self, task_id, owner_id)

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

    postprocess_task(task_id, result_id)
