from celery import Celery
from flask import Flask, request, session
from flask_babel import Babel, lazy_gettext
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

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
bootstrap = Bootstrap(app)
celery = make_celery(app)
babel: Babel = Babel(app)
login_manager = LoginManager(app)
login_manager.localize_callback = lazy_gettext


@babel.localeselector
def get_locale():
    if current_user.is_authenticated:
        return current_user.language

    if 'language' in session:
        return session['language']

    return request.accept_languages.best_match(app.config['LANGUAGES'])


from web import views, models, credentials, profiles, tasks, results, filters
