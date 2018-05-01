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
    submitFulltime = SubmitField("Add Fulltime Employee")
    submitExternal = SubmitField("Add External Employee")

class EditEmployeeForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField("Edit Employee")

class DeleteEmployeeForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    id = FloatField('id', validators=[DataRequired()])
    submit = SubmitField("Delete Employee")

class SeeClassForm(FlaskForm):
    instructorId = FloatField('instructorId',validators = [DataRequired()])
    classId = FloatField('classId',validators=[DataRequired()])
    roomCap = FloatField("roomCap", validators=[DataRequired()])
    submitSeeDetails = SubmitField("See Class Details")

class JoinClassForm(FlaskForm):
    instructorId = FloatField('instructorId',validators = [DataRequired()])
    classId = FloatField('classId',validators=[DataRequired()])
    roomCap = FloatField("roomCap",validators=[DataRequired()])
    submitJoinClass = SubmitField("Join Class")

class checkClassesForm(FlaskForm):
    instructorId = FloatField('instructorId', validators=[DataRequired()])
    classId = FloatField('classId', validators=[DataRequired()])
    roomCap = FloatField("roomCap", validators=[DataRequired()])
    submitCheckClasses = SubmitField("Go back")

class addExerciseForm(FlaskForm):
    exerciseName = StringField("name", validators = [DataRequired()])
    exerciseDescription = StringField("description",validators = [DataRequired()])
    submitAddExercise = SubmitField("Add exercise")

class deleteExerciseForm(FlaskForm):
    exerciseId = FloatField("exerciseId",validators = [DataRequired()])
    exerciseName = StringField("name",validators = [DataRequired()])
    submit = SubmitField("Delete Exercise")
