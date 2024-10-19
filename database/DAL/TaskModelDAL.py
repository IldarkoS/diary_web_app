from sqlalchemy.orm import Session
from database.Models import TaskModel
import datetime

class ModelTaskDAL:
    def __init__(self, Session):
        self.session = Session

    def create_taks(self, title, description, user_id) -> TaskModel:
        task = TaskModel(title=title, description=description, user_id=user_id)
        self.session.add(task)
        self.session.commit()