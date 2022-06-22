from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User

# Pagina 46
class Controle_servo(FlaskForm):
   angulo_H = IntegerField('Horizontal angle')
   angulo_V = IntegerField('Vertical angle')

   submit = SubmitField("Submit specific servo position")


class Controle_cam(FlaskForm):
    view = SubmitField("Ver camera")  
    gravacao = SubmitField("Gravar")  
    movimento = SubmitField("Detectar movimento")  
    rosto = SubmitField("Detectar rosto")