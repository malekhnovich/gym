from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms import validators

class AddEmployeeForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField("Add Employee")


class DeleteEmployeeForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField("Delete Employee")