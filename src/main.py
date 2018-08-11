from flask.cli import AppGroup

from web import app, db
from web.models import User, ScanProfile, ProfileSetting, Task, Control
from control_list import control_list


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        User=User,
        ScanProfile=ScanProfile,
        ProfileSetting=ProfileSetting,
        Task=Task,
    )


control_cli = AppGroup('control')


@control_cli.command('init')
def init_controls():
    Control.query.delete()
    for control in control_list:
        for item in control.data:
            db.session.add(
                Control(
                    number=control.number,
                    language=item['language'],
                    name=item['name'],
                    description=item['description']
                )
            )
    db.session.commit()


app.cli.add_command(control_cli)


if __name__ == '__main__':
    app.run(debug=True)
