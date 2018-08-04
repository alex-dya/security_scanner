import os
from pathlib import Path


class Config:
    TITLE = 'Security Scanner'
    CSRF_ENABLED = True
    SECRET_KEY = 'CHANGE_ME'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f'sqlite:///{Path(Path.cwd(), "app.db")}'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
