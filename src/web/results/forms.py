from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from .exports import generators


class ExportForm(FlaskForm):
    format = SelectField('Format', choices=[
        (name, name)
        for name in generators
    ])
    submit = SubmitField('Export')
