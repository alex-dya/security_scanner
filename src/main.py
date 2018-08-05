from web import app, db
from web.models import User, ScanProfile, ProfileSetting


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'ScanProfile': ScanProfile,
        'ProfileSetting': ProfileSetting
    }


if __name__ == '__main__':
    app.run(debug=True)
