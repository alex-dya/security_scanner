from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, SelectField, IntegerField,
    BooleanField)
from wtforms.validators import (
    DataRequired, IPAddress, NumberRange,  ValidationError, EqualTo, Email)

from web.models import User


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
