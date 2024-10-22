# from flask import Flask
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
# import os, config

# app = Flask(__name__)
# app.config.from_object(config('APP_SETTINGS'))

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# login_manager = LoginManager(app)
# login_manager.login_view = 'login'

# from src.account.views import account_bp
# from src.core.views import core_bp

# app.register_blueprint(accounts_bp)
# app.register_blueprint(core_bp)

# from . import views