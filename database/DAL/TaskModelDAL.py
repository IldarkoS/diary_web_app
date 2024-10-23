from sqlalchemy.orm import Session
from database.Models.TaskModel import TaskModel
import datetime
from extensions import db

def create_task(title, description, user_id) -> TaskModel:
    task = TaskModel(title=title, description=description, user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return task

def get_user_tasks(id) -> list:
    tasks = TaskModel.query.filter(TaskModel.user_id == id).all()
    return tasks