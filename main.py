import config
from flask import Flask, request, render_template, url_for, redirect, flash, make_response
from extensions import db
from database.DAL import TaskModelDAL, UserModelDAL, PlanModelDAL
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from database.Models import UserModel
from forms import LoginForm, TaskForm, RegisterForm, ViewTaskForm, PlanForm, TaskWithPlanForm
from flask_cors import CORS
import time


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config.APP_SECRET_KEY
    connect_to_database(app=app)
    return app


def connect_to_database(app) -> None:
    app.config['SQLALCHEMY_DATABASE_URI'] = config.PSQLURL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app=app)
    
    with app.app_context():
        db.create_all()


app = create_app()
login_manager = LoginManager()
login_manager.init_app(app)
# cors = CORS(app)


@login_manager.user_loader
def load_user(id):
    return UserModel.UserModel.query.get(id)


@app.route("/")
def home():
    return render_template("home.html")


@login_required
@app.route('/view_task/', methods=['GET'])
def get_tasks() -> dict:
    tasks = TaskModelDAL.get_user_tasks(current_user.id)
    form = TaskForm()
    new_task_form = TaskForm()
    return render_template("tasks.html", form=form, tasks=tasks, new_task_form=new_task_form)


@login_required
@app.route('/create_task/', methods=['GET', 'POST'])
def create_tasks():
    tasks = TaskModelDAL.get_user_tasks(current_user.id)
    form = TaskForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_task = TaskModelDAL.create_task(
                title=request.form.get('title'),
                description=request.form.get('description'),
                user_id=current_user.id,
                expired_at=request.form.get('expired_at')
            )
            return redirect(url_for("get_tasks"))
    return render_template("create_task.html", new_task_form=form)


@login_required
@app.route('/view_task/<id>', methods=['GET', "POST"])
def view_task(id):
    task = TaskModelDAL.view_task(id)
    tasks = TaskModelDAL.get_user_tasks(current_user.id)
    form = ViewTaskForm(obj=task)
    new_taks_form = TaskForm()
    if request.method == "POST":
        if form.validate_on_submit():
            title = request.form.get("title")
            description = request.form.get("description")
            completed = True if request.form.get("completed") == 'y' else False
            expired_at = request.form.get("expired_at")
            task = TaskModelDAL.edit_task(task.id, title, description, expired_at, completed)
            return render_template("tasks.html", task=task, form=form, tasks=tasks, new_task_form=new_taks_form)
    return render_template("tasks.html", task=task, form=form, tasks=tasks, new_task_form=new_taks_form)


@login_required
@app.route('/delete_task/<id>', methods=['GET', 'POST'])
def delete_task(id):
    TaskModelDAL.delete_task(id=id)
    return redirect(url_for("get_tasks"))


@login_required
@app.route('/complete_task/<id>', methods=['GET', 'POST'])
def complete_task(id):
    TaskModelDAL.complete_task(id=id)
    return redirect(url_for("get_tasks"))


@app.route('/plans/', methods=['GET'])
@login_required
def view_plans():
    plans = PlanModelDAL.get_plans_by_user(current_user.id)
    return render_template("plans.html", plans=plans)


@app.route('/plans/create/', methods=['GET', 'POST'])
@login_required
def create_plan():
    form = PlanForm()
    if form.validate_on_submit():
        PlanModelDAL.create_plan(
            user_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            expired_at=form.expired_at.data
        )
        return redirect(url_for('view_plans'))
    return render_template("create_plan.html", form=form)


@app.route('/plan/<int:plan_id>', methods=['GET', 'POST'])
@login_required
def view_plan(plan_id):
    plan = PlanModelDAL.get_plan_by_id(plan_id)
    tasks = TaskModelDAL.get_tasks_by_plan(plan_id=plan_id)
    form = TaskWithPlanForm()
    if form.validate_on_submit():
        new_task = TaskModelDAL.create_task(
            title=form.title.data,
            description=form.description.data,
            expired_at=plan.expired_at,
            plan_id=plan_id,
            user_id=current_user.id
        )
        return redirect(url_for('view_plan', plan_id=plan_id))
    return render_template("view_plan.html", plan=plan, tasks=tasks, form=form)


@login_required
@app.route('/delete_task_in_plan/<plan_id>/<id>', methods=['GET', 'POST'])
def delete_task_in_plan(plan_id, id):
    TaskModelDAL.delete_task(id=id)
    return redirect(f"/plan/{plan_id}")


@login_required
@app.route('/complete_task_in_plan/<plan_id>/<id>', methods=['GET', 'POST'])
def complete_task_in_plan(plan_id, id):
    TaskModelDAL.complete_task(id=id)
    return redirect(f"/plan/{plan_id}")


@login_required
@app.route('/delete_plan/<plan_id>', methods=['GET', 'POST'])
def delete_plan(plan_id):
    PlanModelDAL.delete_plan(plan_id=plan_id)
    return redirect(url_for("view_plans"))


@app.route('/plan/<int:plan_id>/update_order', methods=['POST'])
@login_required
def update_task_order(plan_id):
    data = request.json  # Получаем JSON-данные с новым порядком задач
    for index, task_id in enumerate(data.get("task_ids", [])):
        task = TaskModelDAL.view_task(task_id)
        if task and task.plan_id == plan_id:
            task.order = index
    db.session.commit()
    return {"message": "Order updated successfully"}


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = UserModelDAL.get_user_by_email(request.form.get("email"))
            if user and UserModelDAL.check_password(user.id, request.form.get("password")):
                login_user(user, remember=form.remember.data)
                return redirect(url_for("get_tasks"))
            flash("Invalid username or password, try again!", 'error')
    return render_template("login.html", form=form)


@app.route('/register/', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = UserModelDAL.create_user(name=request.form.get("name"),
                        email=request.form.get("email"),
                        password=request.form.get("password"))
            flash(message="Account created!", category="success")
            return redirect(url_for("login"))
    return render_template("sign_up.html", form=form)


@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)