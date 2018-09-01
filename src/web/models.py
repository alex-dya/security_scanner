from collections import defaultdict
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Optional

from celery.app.control import Control as CeleryControl
from celery.result import AsyncResult
from flask_login import UserMixin
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

from scanner.types import ControlStatus
from web import db, login_manager, celery


class TaskStatus(Enum):
    Idle = auto()
    Wait = auto()
    Running = auto()


class ProfileSetting(db.Model):
    __table_args__ = (
        db.UniqueConstraint(
            'transport',
            'setting',
            'profile_id',
            name='profile_setting_uniq'),
    )

    id = db.Column(db.Integer, primary_key=True)
    transport = db.Column(db.String, nullable=False)
    setting = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    profile_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'scan_profile.id',
            ondelete='CASCADE',
            name='profile_setting_fk'
        ),
        nullable=False,
        index=True
    )

    def __repr__(self):
        return f'ProfileSetting(transport={self.transport}, ' \
               f'setting={self.setting})'


class AccountCredential(db.Model):
    __table_args__ = (
        db.UniqueConstraint('name', 'owner_id', name='account_cred_uniq'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), index=True)
    password = db.Column(db.String(128))
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        index=True,
        nullable=False
    )

    def __repr__(self) -> str:
        return f'AccountCredential({self.name})'


class ScanProfile(db.Model):
    __table_args__ = (
        db.UniqueConstraint('name', 'owner_id', name='scan_profile_uniq'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'users.id',
            name='scan_profile_fk',
            ondelete='CASCADE'
        ),
        nullable=False
    )

    settings = db.relationship(
        'ProfileSetting',
        lazy='dynamic',
        cascade="save-update, delete"
    )

    def __repr__(self) -> str:
        return f'ScanProfile(name={self.name})'

    def to_dict(self) -> Dict[str, Dict[str, str]]:
        result = defaultdict(dict)
        for item in self.settings:
            if item.setting == 'credential':
                credential = AccountCredential.query.get(item.value)
                result[item.transport].update(dict(
                    username=credential.username,
                    password=credential.password
                ))
                continue

            result[item.transport][item.setting] = item.value

        return result


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    language = db.Column(db.String(2), default='en')

    credentials = db.relationship(
        'AccountCredential', backref='owner', lazy='dynamic')
    scan_profiles = db.relationship(
        'ScanProfile', backref='owner', lazy='dynamic')
    tasks = db.relationship(
        'Task', backref='owner', lazy='dynamic')
    results = db.relationship(
        'TaskResult',
        backref='owner',
        lazy='dynamic',
        order_by='desc(TaskResult.started)'
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f'User({self.username})'


@login_manager.user_loader
def load_user(id_: str):
    return User.query.get(int(id_))


class TaskSetting(db.Model):
    __table_args__ = (
        db.UniqueConstraint(
            'hostname',
            'profile_id',
            'task_id',
            name='task_setting_uniq'),
    )

    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(128))
    profile_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'scan_profile.id',
            name='task_setting_fk',
            ondelete='SET NULL'
        ),
        nullable=False
    )
    task_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'task.id',
            name='task_setting_fk2',
            ondelete='CASCADE'
        ),
        nullable=False
    )
    profile = db.relationship('ScanProfile')

    def __repr__(self):
        return f'TaskSetting(hostname={self.hostname}, ' \
               f'profile_id={self.profile_id})'


class Task(db.Model):
    __table_args__ = (
        db.UniqueConstraint('name', 'owner_id', name='task_uniq'),
    )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    status = db.Column(
        db.Enum(TaskStatus),
        default=TaskStatus.Idle,
        server_default=TaskStatus.Idle.name,
        nullable=False,
    )
    uid = db.Column(db.String(128))
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'users.id',
            name='task_fk',
            ondelete='CASCADE'
        ),
        nullable=False
    )

    settings = db.relationship(
        'TaskSetting', backref='task', lazy='dynamic')
    results = db.relationship(
        'TaskResult',
        backref='task',
        lazy='dynamic',
        order_by='TaskResult.started'
    )

    def to_list(self) -> List:
        return [
            dict(
                address=item.hostname,
                **item.profile.to_dict()
            )
            for item in self.settings
        ]

    def update_status(self, status: TaskStatus):
        if status == TaskStatus.Wait:
            if self.status != TaskStatus.Idle:
                return

            self.status = TaskStatus.Wait
        elif status == TaskStatus.Idle:
            if self.uid is None:
                self.status = TaskStatus.Idle
                return

            if self.status == TaskStatus.Idle:
                return

            self.status = TaskStatus.Idle
            celery_task = AsyncResult(self.uid)

            if celery_task:
                CeleryControl(celery).revoke(self.uid, terminate=True)

            self.uid = None

    def __repr__(self):
        return f'Task(name={self.name})'


class TaskResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'task.id',
            name='task_result_fk',
            ondelete='SET NULL'
        ),
        nullable=False
    )
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'users.id',
            name='task_fk',
            ondelete='CASCADE'
        ),
        nullable=False
    )
    started = db.Column(
        db.DateTime,
        server_default=func.now()
    )
    finished = db.Column(db.DateTime)
    host_results = db.relationship(
        'HostResult',
        backref='task',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    @property
    def duration(self) -> Optional[datetime]:
        if self.finished is None:
            return

        return self.finished - self.started

    def finish(self):
        self.finished = datetime.utcnow()

    def __repr__(self):
        return f'TaskResult(started="{self.started.isoformat()}")'


class HostResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'task_result.id',
            name='host_result_fk',
            ondelete='CASCADE'
        ),
        nullable=False
    )
    config = db.Column(db.String)
    hostname = db.Column(db.String)

    controls = db.relationship(
        'ControlResult',
        backref='host_result',
        lazy='dynamic',
        order_by='ControlResult.control_number',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'HostResult(hostname={self.hostname})'


class ControlResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host_result_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'host_result.id',
            name='control_result_fk',
            ondelete='CASCADE'
        ),
        nullable=False
    )
    control_number = db.Column(db.Integer, nullable=False)
    status = db.Column(
        db.Enum(ControlStatus),
        nullable=False,
    )
    result = db.Column(db.String)

    def __repr__(self):
        return f'ControlResult(number={self.control_number})'


class Control(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, index=True)
    language = db.Column(db.String(4), server_default='en', index=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(2048), nullable=False)

    def __repr__(self):
        return f'Control(number={self.number}, lang={self.language})'
