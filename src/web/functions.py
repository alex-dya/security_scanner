from time import sleep

from web import celery, models, db, app


def prepare_task(self, task_id):
    task = models.Task.query.get(task_id)
    task.status = models.TaskStatus.Running
    task.uid = self.request.id
    db.session.commit()


def postprocess_task(task_id):
    task = models.Task.query.get(task_id)
    task.status = models.TaskStatus.Idle
    task.uid = None
    db.session.commit()


@celery.task(bind=True)
def summ(self, task_id):
    prepare_task(self, task_id)

    total = 15
    result = 0
    for i in range(total):
        sleep(1)
        result += i
        if not self.request.called_directly:
            app.logger.debug('UPDATE porgress')
            self.update_state(
                state='PROGRESS',
                meta={'current': i, 'total': total}
            )

    postprocess_task(task_id)
