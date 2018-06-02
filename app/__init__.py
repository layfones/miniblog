from flask import Flask
import os
from config import Config
import logging
from logging.handlers import RotatingFileHandler
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

    if not os.path.exists('mylogs'):
        os.mkdir('mylogs')
        print('000')
    print(os.getcwd())
    print('000000')
    file_handler = RotatingFileHandler('mylogs/miniblog.log',
                                       maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Miniblog startup')

    return app


from app import models
