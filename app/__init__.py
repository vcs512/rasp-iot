from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config

# # from app.email import send_async_email
# from flask_mail import Message
# import os

# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    # print(f'Config={config[config_name].APPLICATION_ROOT}')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # print(f"APPLICATION_ROOT={app.config['APPLICATION_ROOT']}")
    # app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    # app.config['MAIL_PORT'] = 587
    # app.config['MAIL_USE_TLS'] = True
    # # app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    # # app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    # msg = Message('hello', sender='vigisel0373@gmail.com', recipients=['emailfulano@.com'])
    # send_async_email(app, msg)

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .camera import cam as cam_blueprint
    app.register_blueprint(cam_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
