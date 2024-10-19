import config
from flask import Flask, request, render_template
from extensions import db
from database.DAL import TaskModelDAL, UserModelDAL

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


@app.route('/')
def view_form():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)