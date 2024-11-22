from sqlalchemy.orm import Session
from database.Models.TaskModel import TaskModel
import datetime
from extensions import db

def create_task(title, description, user_id, expired_at, plan_id = None) -> TaskModel:
    task = TaskModel(title=title, description=description, user_id=user_id, expired_at=expired_at, plan_id=plan_id)
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


def view_task(id) -> TaskModel():
    task = TaskModel.query.filter(TaskModel.id == id).first()
    return task

def edit_task(id, title, description, expired_at, completed):
    task = TaskModel.query.filter(TaskModel.id == id).first()
    task.title = title
    task.description = description
    task.expired_at = expired_at
    task.completed = completed
    db.session.commit()
    return task

def set_task_order(task_id, order):
    task = TaskModel.query.get(task_id)
    if task:
        task.order = order
        db.session.commit()

def get_tasks_by_plan(plan_id):
    return TaskModel.query.filter_by(plan_id=plan_id).order_by(TaskModel.order).all()
