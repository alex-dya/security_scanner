from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, SelectField, IntegerField)
from wtforms.validators import DataRequired, IPAddress, NumberRange


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
