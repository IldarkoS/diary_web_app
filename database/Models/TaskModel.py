from sqlalchemy.orm import validates
from extensions import db
from werkzeug.routing import ValidationError
import datetime


class TaskModel(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255),nullable=False)
    description = db.Column(db.String,nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    expired_at = db.Column(db.DateTime, default=datetime.datetime.now())


    @validates
    def validate_title(self, key, title):
        if not title:
            raise ValidationError('title can not be empty')
        if not isinstance(title, str):
            raise ValidationError('title must be a string')
        if len(title) > 250:
            raise ValidationError('title lenght must be less than 250')

    @validates
    def validate_description(self, key, description):
        if not description:
            raise ValidationError('description can not be empty')
        if not isinstance(description, str):
            raise ValidationError('description must be a string')
        if len(description) > 2**10:
            raise ValidationError('description lenght must be less than 250')