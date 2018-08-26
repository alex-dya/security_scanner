from celery import Celery
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_bootstrap import Bootstrap
from flask_babel import Babel

from config import Config


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend='db+' + app.config['SQLALCHEMY_DATABASE_URI'],
        broker=app.config['CELERY_BROKER_URL'],
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
bootstrap = Bootstrap(app)
celery = make_celery(app)
babel = Babel(app)


@babel.localeselector
def get_locale():
    if current_user.is_authenticated:
        return current_user.language

    return request.accept_languages.best_match(app.config['LANGUAGES'])


from web import views, models, credentials, profiles, tasks, results, filters
