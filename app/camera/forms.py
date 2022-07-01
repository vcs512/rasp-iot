from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, IntegerField, FloatField, RadioField
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


class cv_motion(FlaskForm):
    '''adjust motion detection'''
    adjust_motion = RadioField('Motion adjust', choices=[('1','Default'),('2','Best movement accommodation, less accuracy'), ('3','More accuracy and sensitivity')])
    submit = SubmitField("Submit predefined motion profile")


class cv_hist(FlaskForm):
    '''adjust number of frames for history in motion detection'''

    history = IntegerField('Number of past frames to considerate', validators=[NumberRange(min=1, max=1e6, message='Enter range between {} and {}'.format(1, 1e6))])
    submit = SubmitField("Submit number of past frames")

class cv_dk(FlaskForm):
    '''adjust kernel size in motion detection'''

    dk = IntegerField('Kernel size', validators=[NumberRange(min=1, max=200, message='Enter range between {} and {}'.format(1, 200))])
    submit = SubmitField("Submit kernel size")    

class cv_lim_bin(FlaskForm):
    '''adjust kernel size in motion detection'''

    lim = IntegerField('Threshold value', validators=[NumberRange(min=5, max=250, message='Enter range between {} and {}'.format(5, 250))])
    submit = SubmitField("Submit threshold value")



class cv_face(FlaskForm):
    '''adjust face detection'''
    adjust_face = RadioField('Face detection adjust', choices=[('1','Default'),('2','Smaller faces, more intensive'), ('3','More accuracy')])
    submit = SubmitField("Submit predefined fece detection profile")

class cv_scale(FlaskForm):
    '''adjust scale factor in face detection'''

    scale = FloatField('Scale factor', validators=[NumberRange(min=0.5, max=5, message='Enter range between {} and {}'.format(0.5, 5))])
    submit = SubmitField("Submit scale factor")    

class cv_min_neig(FlaskForm):
    '''minimum Neighbors in face detection'''

    min = IntegerField('Minimum Neighbors', validators=[NumberRange(min=2, max=40, message='Enter range between {} and {}'.format(2, 40))])
    submit = SubmitField("Submit minimum neighbors")       