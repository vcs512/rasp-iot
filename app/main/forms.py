from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, PasswordField
from wtforms.validators import DataRequired
from ..models import Role, User


class TrocaRole(FlaskForm):
    role = RadioField('User new role', choices=[('1','Commom user'),('2','Moderator')])
    submit = SubmitField('Submit new role')

class ExcluirUser(FlaskForm):
    password = PasswordField('Password for ADMIN', validators=[DataRequired()])
    submit = SubmitField('Exclude user')    