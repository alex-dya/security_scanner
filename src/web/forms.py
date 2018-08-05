from collections import defaultdict
from typing import Dict

from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, SelectField, IntegerField,
    BooleanField, HiddenField, FormField)
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import (
    DataRequired, IPAddress, NumberRange, ValidationError, EqualTo, Email)

from scanner.transports.unix import RootLogonType
from web.models import User, AccountCredential, ScanProfile, ProfileSetting
from web.utlity import get_credentials


class StartTaskForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired()],
        default='vmuser'
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()],
        default='P@ssw0rd'
    )
    hostname = StringField(
        'Hostname',
        validators=[DataRequired(), IPAddress()],
        default='192.168.56.10'
    )
    port = IntegerField(
        'Port',
        validators=[DataRequired(), NumberRange(min=0, max=65535)],
        default=22
    )
    root_logon = SelectField(
        'Escalation method',
        choices=[('SudoLogon', 'Sudo'), ('SULogon', 'SU'), ('NoLogon', 'No')],
        validators=[DataRequired()],
        default='SudoLogon'
    )
    root_password = PasswordField(
        'Root Password',
        validators=[DataRequired()],
        default='P@ssw0rd'
    )
    submit = SubmitField('Run task')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditCredentialForm(FlaskForm):
    id = HiddenField('Id')
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Add')


class SSHSettings(FlaskForm):
    port = IntegerField(
        'Port',
        validators=[DataRequired(), NumberRange(min=0, max=65535)],
        default=22
    )
    credential = QuerySelectField(
        'Credentials',
        get_label='username',
        query_factory=get_credentials
    )

    def populate(self, settings: Dict[str, Dict[str, str]]) -> None:
        ssh_setting = settings['ssh']
        self.port.data = int(ssh_setting.get('port') or 22)
        cred = ssh_setting.get('credential')
        if cred:
            self.credential.data = AccountCredential.query.get(int(cred))


class UnixSettings(FlaskForm):
    privilege_escalation = SelectField('Privilege escalation', choices=[
        (item.name, item.name)
        for item in RootLogonType
    ], default='NoLogon')
    root_password = StringField('Password')

    def populate(self, settings: Dict[str, Dict[str, str]]) -> None:
        self.privilege_escalation.data = settings['unix'].get(
            'privilege_escalation')
        self.root_password.data = settings['unix'].get('root_password')


class ScanProfileForm(FlaskForm):
    id = HiddenField('Id')
    name = StringField('Name', validators=[DataRequired()])
    ssh_settings = FormField(SSHSettings)
    unix_settings = FormField(UnixSettings)
    submit = SubmitField('Save')

    def populate(self, profile: ScanProfile = None) -> None:
        self.name.data = profile.name
        settings = defaultdict(dict)

        for item in profile.settings:
            settings[item.transport][item.setting] = item.value

        self.ssh_settings.populate(settings)
        self.unix_settings.populate(settings)

    def populate_obj(self, profile: ScanProfile) -> None:
        profile.name = self.name.data
        settings = {
            (item.transport, item.setting): item
            for item in profile.settings
        }

        all_settings = [
            ('ssh', 'port', self.ssh_settings.port),
            ('ssh', 'credential', self.ssh_settings.credential),
            ('unix', 'privilege_escalation',
             self.unix_settings.privilege_escalation),
            ('unix', 'root_password', self.unix_settings.root_password),
        ]

        for transport, option, field in all_settings:
            setting = settings.get((transport, option))
            if setting is None:
                setting = ProfileSetting(
                    transport=transport,
                    setting=option,
                    profile_id=profile.id
                )
                profile.settings.append(setting)

            if isinstance(field.data, AccountCredential):
                value = str(field.data.id)
            else:
                value = str(field.data)
            setting.value = value
