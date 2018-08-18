from pathlib import Path

from flask.cli import AppGroup
import yaml

from web import app, db
from web.models import User, ScanProfile, ProfileSetting, Task, Control


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
    control_path = Path(__file__).parent.joinpath('control_list')
    for file in control_path.glob('*.yaml'):
        if file.name == '__blank__.yaml':
            continue

        with file.open('r') as f:
            control = yaml.load(f)

        for item in control['content']:
            db.session.add(
                Control(
                    number=control['number'],
                    language=item['language'],
                    name=item['name'],
                    description=item['description']
                )
            )
    db.session.commit()


app.cli.add_command(control_cli)


if __name__ == '__main__':
    app.run()
