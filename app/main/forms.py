from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField
from ..models import Role, User


class TrocaRole(FlaskForm):
    role = RadioField('User new role', choices=[('1','Commom user'),('2','Moderator')])
    submit = SubmitField('Submit new role')