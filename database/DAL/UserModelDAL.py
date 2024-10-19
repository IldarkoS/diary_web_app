from sqlalchemy.orm import Session
from database.Models.UserModel import UserModel


class UserModelDAL:
    def __init__(self, Session):
        self.session = Session

    def create_user(self, name, email, password) -> UserModel:
        user = UserModel(name=name, email=email, password=password)
        self.session.add(user)
        self.session.commit()
        return user

    