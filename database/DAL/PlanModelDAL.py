from extensions import db
from database.Models.PlanModel import PlanModel
from database.Models.TaskModel import TaskModel

def create_plan(user_id, title, description, expired_at):
    plan = PlanModel(user_id=user_id, title=title, description=description, expired_at=expired_at)
    db.session.add(plan)
    db.session.commit()
    return plan

def get_plans_by_user(user_id):
    return PlanModel.query.filter_by(user_id=user_id).all()

def get_plan_by_id(plan_id):
    return PlanModel.query.get(plan_id)

def add_task_to_plan(plan_id, task_id):
    task = TaskModel.query.get(task_id)
    if task:
        task.plan_id = plan_id
        db.session.commit()

def delete_plan(plan_id):
    PlanModel.query.filter_by(id=plan_id).delete()
    db.session.commit()

def get_sorted_plans_by_user(user_id):
    plans = PlanModel.query.filter_by(user_id=user_id).all()
    return sorted(plans, key=lambda plan: plan.is_completed())
