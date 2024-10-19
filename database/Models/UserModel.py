from sqlalchemy.orm import validates
from extensions import db
from werkzeug.routing import ValidationError


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),nullable=False)
    email = db.Column(db.String(255),nullable=False)
    password = db.Column(db.String(255),nullable=False)

    @validates
    def validate_name(self, key, name):
        if not name:
            raise ValidationError('Name can not be empty')
        if not isinstance(name, str):
            raise ValidationError('Name must be a string')
        if len(name) > 250:
            raise ValidationError('Name lenght must be less than 250')
        

    @validates
    def validate_email(self, key, email):
        if not email:
            raise ValidationError('Email can not be empty')
        if not isinstance(email, str):
            raise ValidationError('Email must be a string')
        if len(email) > 250:
            raise ValidationError('Email lenght must be less than 250')
        