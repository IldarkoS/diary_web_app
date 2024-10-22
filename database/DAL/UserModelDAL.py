from sqlalchemy.orm import Session
from database.Models.UserModel import UserModel
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

def create_user(name, email, password) -> UserModel:
    user = UserModel(name=name, email=email, hashed_password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return user

def set_password(id, new_pass) -> bool:
    user = UserModel.query.filter(UserModel.id == id).first()
    user.hashed_password = generate_password_hash(new_pass)
    db.session.commit()
    return True

def check_password(id, password) -> bool:
    user = UserModel.query.filter(UserModel.id == id).first()
    return check_password_hash(user.hashed_password, password)

def get_all_users() -> list:
    users = UserModel.query.filter(id is not None).all()
    return users

def get_user_by_email(email) -> UserModel:
    user = UserModel.query.filter(UserModel.email == email).first()
    return user