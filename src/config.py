import os


class Config:
    TITLE = 'Security Scanner'
    CSRF_ENABLED = True
    SECRET_KEY = 'CHANGE_ME'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f'postgresql://postgres:P@ssw0rd@localhost:5432/scanner'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'amqp://scanner:P@ssw0rd@localhost:5672/scanner'
