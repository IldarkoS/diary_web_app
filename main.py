import config
from flask import Flask, request, render_template, url_for, redirect, flash, make_response
from extensions import db
from database.DAL import TaskModelDAL, UserModelDAL
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from database.Models import UserModel
from forms import LoginForm, TaskForm, RegisterForm
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


@login_manager.user_loader
def load_user(id):
    return UserModel.UserModel.query.get(id)


@app.route("/")
def home():
    return render_template("home.html")


@login_required
@app.route('/tasks/', methods=['GET'])
def get_tasks() -> dict:
    tasks = TaskModelDAL.get_user_tasks(current_user.id)
    return render_template("tasks.html", tasks=tasks)


@login_required
@app.route('/create_task/', methods=['GET', 'POST'])
def create_tasks():
    form = TaskForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_task = TaskModelDAL.create_task(
                title=request.form.get('title'),
                description=request.form.get('description'),
                user_id=current_user.id,
                expired_at=request.form.get('entrydate')
            )
            return redirect(url_for("get_tasks"))
    return render_template("create_task.html", form=form)


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


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = UserModelDAL.get_user_by_email(request.form.get("email"))
            if user and UserModelDAL.check_password(user.id, request.form.get("password")):
                login_user(user, remember=form.remember.data)
                return redirect(url_for("home"))
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