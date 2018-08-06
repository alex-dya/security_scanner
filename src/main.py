from web import app, db
from web.models import User, ScanProfile, ProfileSetting, Task


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        User=User,
        ScanProfile=ScanProfile,
        ProfileSetting=ProfileSetting,
        Task=Task,
    )


if __name__ == '__main__':
    app.run(debug=True)
