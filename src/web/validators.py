from flask_babel import lazy_gettext as _l
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import Field
from wtforms.validators import (
    ValidationError, HostnameValidation, DataRequired, Optional)

from web import db


class UniqueRequired:
    def __init__(self, model: db.Model, field: str):
        self.field = field
        self.model = model

    def __call__(self, form, field):
        if not field.data:
            return

        current_item = None
        if form.id.data:
            current_item = self.model.query.get(form.id.data)

        item = self.model.query.filter_by(
            **{self.field: field.data, 'owner_id': current_user.get_id()}
        ).scalar()

        if item and item != current_item:
            raise ValidationError(
                _l(
                    'Field %(text)s must have unique value',
                    text=field.label.text
                )
            )


class HostnameRequired:
    def __init__(self, message: str = None, **kwargs):
        self.message = (
                message or 'This field must contain hostname or IP address')
        self.validator = HostnameValidation(**kwargs)

    def __call__(self, form, field):
        if not field.data:
            raise ValidationError(_l(self.message))

        if not isinstance(field.data, str):
            raise ValidationError(_l(self.message))

        if not self.validator(field.data):
            raise ValidationError(_l(self.message))


class RequiredIf:
    """
    Validator which makes a field required if another field is set
    and has a correct value.
    """
    field_flags = ('requiredif',)

    def __init__(self, message=None, **kwargs):
        self.message = message
        self.fields = kwargs

    def __call__(self, form: FlaskForm, field: Field):
        for name, value in self.fields.items():
            other_field = form[name]
            if other_field is None:
                raise ValueError(
                    f'There is not a field {name} in form '
                    f'{form.__class__.__name__}')

            if other_field.data == value:
                DataRequired(message=self.message)(form, field)
        else:
            Optional()(form, field)
