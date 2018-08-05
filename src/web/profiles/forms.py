from collections import defaultdict
from typing import Dict

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    IntegerField, SelectField, StringField, HiddenField, FormField, SubmitField)
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, NumberRange

from scanner.transports.unix import RootLogonType
from web.models import AccountCredential, ScanProfile, ProfileSetting


def get_credentials():
    return current_user.credentials


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

