from sqlalchemy.orm import validates
from extensions import db
from werkzeug.routing import ValidationError
from flask_login import (LoginManager, UserMixin, login_required, login_user, current_user, logout_user)
from main import login_manager


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(UserModel).get(id=user_id)

class UserModel(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255),nullable=False)
    email = db.Column(db.String(255),nullable=False)
    hashed_password = db.Column(db.String(255),nullable=False)

    def __repr__(self) -> str:
        return "<>:<>".format(self.id, self.name)
    

    @validates
    def validate_name(self, key, name) -> None:
        if not name:
            raise ValidationError('Name can not be empty')
        if not isinstance(name, str):
            raise ValidationError('Name must be a string')
        if len(name) > 250:
            raise ValidationError('Name lenght must be less than 250')
        

    @validates
    def validate_email(self, key, email) -> None:
        if not email:
            raise ValidationError('Email can not be empty')
        if not isinstance(email, str):
            raise ValidationError('Email must be a string')
        if len(email) > 250:
            raise ValidationError('Email lenght must be less than 250')
        
    