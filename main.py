import config
from flask import Flask, request, render_template, url_for, redirect, flash
from extensions import db
from database.DAL import TaskModelDAL, UserModelDAL
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from database.Models import UserModel

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


@app.route('/admin/')
@login_required
def admin():
    return render_template('admin.html')


@app.route('/tasks', methods=['GET'])
def get_tasks(user_id) -> dict:
    pass

@app.route('/users', methods=['GET'])
def get_users() -> dict:
    users = UserModelDAL.get_all_users()
    ans = {'Users':[]}
    for each in users:
        ans['Users'].append({
            "id": each.id,
            "name": each.name
        })
    return ans


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = UserModelDAL.get_user_by_email(request.form.get("email"))
        if user and UserModelDAL.check_password(user.id, request.form.get("password")):
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = UserModelDAL.create_user(name=request.form.get("username"),
                    email=request.form.get("email"),
                    password=request.form.get("password"))
        return redirect(url_for("login"))
    return render_template("sign_up.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)