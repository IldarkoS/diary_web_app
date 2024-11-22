from extensions import db
import datetime

class PlanModel(db.Model):
    __tablename__ = 'plans'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    expired_at = db.Column(db.DateTime, default=datetime.datetime.now())
    tasks = db.relationship('TaskModel', backref='plan',cascade='all, delete', lazy=True)

    def is_completed(self):
        return all(task.completed for task in self.tasks)

    def progress(self):
        if not self.tasks:
            return 0
        completed = sum(1 for task in self.tasks if task.completed)
        return int((completed / len(self.tasks)) * 100)