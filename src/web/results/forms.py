from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import SelectField, SubmitField
from .exports import generators


class ExportForm(FlaskForm):
    format = SelectField(_l('Format'), choices=[
        (name, name)
        for name in generators
    ])
    submit = SubmitField(_l('Export'))
