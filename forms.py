from flask_wtf import FlaskForm
from wtforms import Form, ValidationError
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email
import email_validator

class LoginForm(FlaskForm):
    email = StringField("E-mail: ", validators=[Email()])
    password = StringField("Password: ", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField()

class TaskForm(FlaskForm):
    title = StringField("Title:", validators=[DataRequired()])
    description = StringField("Description: ", validators=[DataRequired()])
    submit = SubmitField()
    