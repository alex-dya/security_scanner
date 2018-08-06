from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

from web import models
from web.validators import UniqueRequired


class EditCredentialForm(FlaskForm):
    id = HiddenField('Id')
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            UniqueRequired(models.AccountCredential, 'name')
        ]
    )
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Save')
