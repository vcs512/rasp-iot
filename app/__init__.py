from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config

# from flask_mqtt import Mqtt
# import random

# import eventlet
# import json
# # from flask import Flask, render_template
# from flask_mqtt import Mqtt
# from flask_socketio import SocketIO
# # from flask_bootstrap import Bootstrap

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
# mqtt = Mqtt()
# eventlet.monkey_patch()

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
    
    # mqtt.init_app(app)
    # socketio = SocketIO(app)

    # msg = Message('hello', sender='vigisel0373@gmail.com', recipients=['emailfulano@.com'])
    # send_async_email(app, msg)

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    # # configurar MQTT
    # app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
    # app.config['MQTT_BROKER_PORT'] = 1883
    # app.config['MQTT_CLIENT_ID'] = f'python-mqtt-{random.randint(0, 100)}'
    # app.config['MQTT_KEEPALIVE'] = 600
    # app.config['MQTT_TLS_ENLABLED'] = False
    # app.config['MQTT_LAST_WILL_TOPIC'] = 'Topic_LastWill'
    # app.config['MQTT_LAST_WILL_MESSAGE'] = 'LastWill_message'
    # app.config['MQTT_LAST_WILL_QOS'] = 0

    # app.config['MQTT_USERNAME'] = 'emqx'
    # app.config['MQTT_PASSWORD'] = 'public'

    # mqtt.subscribe('Motion')

    # @mqtt.on_message()
    # def handle_mqtt_message(client, userdata, message):
    #     data = dict(
    #         topic=message.topic,
    #         payload=message.payload.decode()
    #     )
    #     print('Received message on topic {}: {}'
    #     .format(message.topic, message.payload.decode()))

    # # mqtt.publish('Motion', 'abriu camera')


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .camera import cam as cam_blueprint
    app.register_blueprint(cam_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
