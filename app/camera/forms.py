from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, IntegerField
from wtforms.fields.html5 import IntegerRangeField

from wtforms.validators import DataRequired, Length, Email, Regexp, NumberRange
from wtforms import ValidationError

from flask_pagedown.fields import PageDownField
from ..models import Role, User

from app.camera.servo import Servo_Control


# Pagina 46
class Controle_servo(FlaskForm):
    '''adjust servos with integers'''

    angulo_H = IntegerField('Horizontal angle', validators=[NumberRange(min=Servo_Control.min_H, max=Servo_Control.max_H, message='Enter range between {} and {}'.format(Servo_Control.min_H, Servo_Control.max_H))])
    submit_H = SubmitField("Submit horizontal")

    angulo_V = IntegerField('Vertical angle', validators=[NumberRange(min=Servo_Control.min_V, max=Servo_Control.max_V, message='Enter range between {} and {}'.format(Servo_Control.min_V, Servo_Control.max_V))])
    submit_V = SubmitField("Submit vertical")

    submit = SubmitField("Submit Horizontal and Vertical")

class Servo_H(FlaskForm):
    '''adjust H servo with integers'''

    angulo_H = IntegerField('Horizontal angle', validators=[NumberRange(min=Servo_Control.min_H, max=Servo_Control.max_H, message='Enter range between {} and {}'.format(Servo_Control.min_H, Servo_Control.max_H))])
    submit_H = SubmitField("Submit horizontal")

class Servo_V(FlaskForm):
    '''adjust V servo with integers'''

    angulo_V = IntegerField('Vertical angle', validators=[NumberRange(min=Servo_Control.min_V, max=Servo_Control.max_V, message='Enter range between {} and {}'.format(Servo_Control.min_V, Servo_Control.max_V))])
    submit_V = SubmitField("Submit vertical")


class Servo_adjust(FlaskForm):
    '''adjust servos with sliders'''
    
    angulo_H = IntegerRangeField('Horizontal angle', validators=[NumberRange(min=Servo_Control.min_H, max=Servo_Control.max_H, message='Enter range between {} and {}'.format(Servo_Control.min_H, Servo_Control.max_H))])
    # submit_H = SubmitField("Submit horizontal")

    angulo_V = IntegerRangeField('Vertical angle', validators=[NumberRange(min=Servo_Control.min_V, max=Servo_Control.max_V, message='Enter range between {} and {}'.format(Servo_Control.min_V, Servo_Control.max_V))])
    # submit_V = SubmitField("Submit vertical")

    submit = SubmitField("Submit Horizontal and Vertical")