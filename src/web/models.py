from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from web import db, login_manager


class ProfileSetting(db.Model):
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

    db.UniqueConstraint('transport', 'setting', 'profile_id', name='uix_1')

    def __repr__(self):
        return f'ProfileSetting(transport={self.transport}, ' \
               f'setting={self.setting}'


class AccountCredential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        index=True,
        nullable=False
    )

    def __repr__(self) -> str:
        return f'AccountCredential({self.username})'


class ScanProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'user.id',
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

    db.UniqueConstraint('name', 'owner_id', name='uix_1')

    def __repr__(self) -> str:
        return f'ScanProfile(name={self.name})'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    credentials = db.relationship(
        'AccountCredential', backref='owner', lazy='dynamic')
    scan_profiles = db.relationship(
        'ScanProfile', backref='owner', lazy='dynamic')

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f'User({self.username})'


@login_manager.user_loader
def load_user(id_: str):
    return User.query.get(int(id_))
