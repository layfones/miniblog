from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment

# app = Flask(__name__,  template_folder='../templates', static_folder="", static_url_path="")
# app.config.from_object(Config)

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# login = LoginManager(app)
# mail = Mail(app)
# bootstrap = Bootstrap(app)
# moment = Moment(app)


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
# Flask-Login需要知道哪个视图函数用于处理登录认证
# 'login'值是登录视图函数（endpoint）名
login.login_view = 'auth.login'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    # from app.errors import errors as errors_bp
    # app.register_blueprint(errors_bp)

    from app.auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import main as main_bp
    app.register_blueprint(main_bp)

    from app.api import api as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


from app import models
