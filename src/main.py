from operator import attrgetter
from pathlib import Path

import yaml
from flask.cli import AppGroup

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
        Control=Control,
    )


control_cli = AppGroup('control')


def get_controls():
    control_path = Path(__file__).parent.joinpath('control_list')
    for file in control_path.glob('*.yaml'):
        if file.name == '__blank__.yaml':
            continue

        with file.open('r') as f:
            control = yaml.load(f)

        for item in control['content']:
            yield Control(
                number=control['number'],
                language=item['language'],
                name=item['name'],
                description=item['description']
            )


@control_cli.command('init')
def init_controls():
    Control.query.delete()
    for control in get_controls():
        db.session.add(control)

    db.session.commit()


@app.cli.command('initsql')
def init_sql():
    from sqlalchemy import create_engine
    from sqlalchemy.dialects import postgresql

    def convert_to_sql(file):
        def dump(sql, *multiparams, **params):
            print(f'{str(sql.compile(dialect=postgresql.dialect())).strip()};',
                  file=file)

        engine = create_engine('postgresql://', strategy='mock', executor=dump)
        db.metadata.create_all(engine, checkfirst=False)
        sorted_controls = sorted(get_controls(), key=attrgetter('number', 'language'))
        for id_, control in enumerate(sorted_controls, 1):
            print(f"INSERT INTO control (id, number, language, name, "
                  f"description) VALUES ({id_}, {control.number}, "
                  f"'{control.language}', E{control.name!r}, "
                  f"E{control.description!r});",
                  file=file)

    with open('../init.sql', 'w') as f:
        convert_to_sql(f)


app.cli.add_command(control_cli)

if __name__ == '__main__':
    app.run()
