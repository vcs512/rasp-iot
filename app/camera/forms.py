from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User

# Pagina 46
class Controle_servo(FlaskForm):
   angulo_H = IntegerField('Ângulo horizontal')
   angulo_V = IntegerField('Ângulo vertical')

   submit = SubmitField("Send")