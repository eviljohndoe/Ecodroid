from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired
from app.models import Project


def has_space(string, msg):
    if " " in string:
        raise ValidationError(msg)


class ProjectForm(FlaskForm):
    name = StringField('', validators=[DataRequired()])
    submit = SubmitField('Add project')

    def validate_name(self, name):
        project = Project.query.filter_by(name=name.data.lower()).first()
        if project is not None:
            raise ValidationError("This project already exists")
        has_space(name.data, "Please use \"_\" instead of space in project name")


class EditProjectForm(FlaskForm):
    name = StringField('New name', validators=[DataRequired()])
    submit = SubmitField('Edit project name')

    def __init__(self, old_name, *args, **kwargs):
        super(EditProjectForm, self).__init__(*args, **kwargs)
        self.old_name = old_name

    def validate_name(self, name):
        if name.data.lower() != self.old_name.lower():
            project = Project.query.filter_by(name=name.data.lower()).first()
            if project is not None:
                raise ValidationError("Use a different name")
            has_space(name.data, "Please use \"_\" instead of space in project name")
        else:
            raise ValidationError("The project is already named {}".format(name.data.upper()))
