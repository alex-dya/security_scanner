from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, FormField, HiddenField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, HostnameValidation, ValidationError


def get_profiles():
    return current_user.scan_profiles


class HostnameRequired:
    def __init__(self, message: str = None):
        self.message = (
                message or 'This field must contain hostname or IP address')
        self.validator = HostnameValidation()

    def __call__(self, form, field):
        if not field.data:
            raise ValidationError(self.message)

        if not isinstance(field.data, str):
            raise ValidationError(self.message)

        if not self.validator(field.data):
            raise ValidationError(self.message)


class TaskSettingForm(FlaskForm):
    hostname = StringField('Hostname', validators=[HostnameRequired()])
    profile = QuerySelectField(
        'Profile',
        get_label='name',
        query_factory=get_profiles
    )

    def __init__(self, *args, **kwargs):
        super().__init__(csrf_enabled=False, *args, **kwargs)


class TaskForm(FlaskForm):
    id = HiddenField('Id')
    name = StringField('Name', validators=[DataRequired()])
    settings = FieldList(FormField(TaskSettingForm))
    submit = SubmitField('Save')

    def populate(self, task):
        self.id.data = task.id
        self.name.data = task.name
        for setting in task.settings:
            setting_form = TaskSettingForm()
            setting_form.hostname = setting.hostname
            setting_form.profile = setting.profile
            self.settings.append_entry(setting_form)
