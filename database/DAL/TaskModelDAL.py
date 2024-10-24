from sqlalchemy.orm import Session
from database.Models.TaskModel import TaskModel
import datetime
from extensions import db

def create_task(title, description, user_id, expired_at) -> TaskModel:
    task = TaskModel(title=title, description=description, user_id=user_id, expired_at=expired_at)
    db.session.add(task)
    db.session.commit()
    return task


def delete_task(id):
    TaskModel.query.filter(TaskModel.id==id).delete()
    db.session.commit()


def complete_task(id):
    task = TaskModel.query.filter(TaskModel.id==id).first()
    task.completed = True if task.completed == False else False
    db.session.commit()


def get_user_tasks(id) -> list:
    tasks = TaskModel.query.filter(TaskModel.user_id == id).all()
    return tasks