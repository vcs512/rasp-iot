from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp, NumberRange
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User

from app.camera.servo import Servo_Control

# Pagina 46
class Controle_servo(FlaskForm):
    angulo_H = IntegerField('Horizontal angle', validators=[NumberRange(min=Servo_Control.min_H, max=Servo_Control.max_H, message='Enter range between {} and {}'.format(Servo_Control.min_H, Servo_Control.max_H))])
    # submit_H = SubmitField("Submit horizontal")

    angulo_V = IntegerField('Vertical angle', validators=[NumberRange(min=Servo_Control.min_V, max=Servo_Control.max_V, message='Enter range between {} and {}'.format(Servo_Control.min_V, Servo_Control.max_V))])
    # submit_V = SubmitField("Submit vertical")

    submit = SubmitField("Submit Horizontal and Vertical")


class Controle_cam(FlaskForm):
    view = SubmitField("Ver camera")  
    gravacao = SubmitField("Gravar")  
    movimento = SubmitField("Detectar movimento")  
    rosto = SubmitField("Detectar rosto")