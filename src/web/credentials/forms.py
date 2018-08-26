from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import HiddenField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

from web import models
from web.validators import UniqueRequired


class EditCredentialForm(FlaskForm):
    id = HiddenField(_l('Id'))
    name = StringField(
        _l('Name'),
        validators=[
            DataRequired(),
            UniqueRequired(models.AccountCredential, 'name')
        ]
    )
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Save'))
