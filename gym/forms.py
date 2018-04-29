from flask_wtf import FlaskForm
from wtforms import FloatField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms import validators

class AddEmployeeForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    type = StringField('type',validators = [DataRequired()])
    salary = FloatField('salary', validators = [[DataRequired()]])
    hourlyWage = FloatField('hourlyWage', validators=[[DataRequired()]])
    hours  = FloatField('hours',validators = [[DataRequired()]])
    submit = SubmitField("Add Employee")


class DeleteEmployeeForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField("Delete Employee")