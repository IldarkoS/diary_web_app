from flask_wtf import FlaskForm
from wtforms import Form, ValidationError
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email
from wtforms.fields import DateField
import datetime
import email_validator

class LoginForm(FlaskForm):
    email = StringField("E-mail: ", validators=[Email()])
    password = StringField("Password: ", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField()

class TaskForm(FlaskForm):
    title = StringField("Title:", validators=[DataRequired()])
    description = StringField("Description: ", validators=[DataRequired()])
    entrydate = DateField('Expire Date: ', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField()

    def validate_entrydate(form, field):
        if field.data < datetime.datetime.now().date():
            raise ValidationError("Expired date must not be early than now!")
    

class RegisterForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    email = StringField("E-mail: ", validators=[Email()])
    password = StringField("Password: ", validators=[DataRequired()])
    submit = SubmitField()


class ViewTaskForm(FlaskForm):
    title = StringField("Title: ", validators=[DataRequired()])
    description = StringField("Description: ", validators=[DataRequired()])
    expired_at = DateField('Expire Date: ', format='%Y-%m-%d' )
    completed = BooleanField("Compeleted: ")
    submit = SubmitField()

    def validate_entrydate(form, field):
        if field.data < datetime.datetime.now().date():
            raise ValidationError("Expired date must not be early than now!")