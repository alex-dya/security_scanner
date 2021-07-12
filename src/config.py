import os


class Config:
    TITLE = 'Security Scanner'
    CSRF_ENABLED = True
    SECRET_KEY = 'CHANGE_ME'
    DEBUG = True
    BOOTSTRAP_SERVE_LOCAL = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f'postgresql://postgres:Passw0rd@127.0.0.1:5432/scanner'
    )
    LANGUAGES = ['en', 'ru']

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'amqp://scanner:Passw0rd@broker:5672/scanner'
