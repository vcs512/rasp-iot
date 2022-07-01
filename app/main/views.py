from crypt import methods
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response

from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from . import main
from .forms import TrocaRole
from .. import db
from ..models import Permission, Role, User
from ..decorators import admin_required, permission_required


# ADMIN forced shutdown
@main.route('/shutdown')
@admin_required
def server_shutdown():
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Forced shutdown'


# homepage
@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# user management
@main.route('/moderate/', methods=['GET'])
@login_required
@permission_required(Permission.ADMIN)
def moderate():
    rows = User.query.all()
    return render_template('moderate.html', rows=rows)


# switch role page
@main.route('/moderate/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADMIN)
def moderate_number(id):
    form = TrocaRole()
    usuario = User.query.get_or_404(id)

    # if ADMIN scapes
    if usuario.role_id == 3:
        return redirect('/moderate')
    
    if form.validate_on_submit():
        role = form.role.data
        role = int(role)
        
        usuario = User.query.get_or_404(id)
        usuario.role_id = role

        try:
            db.session.add(usuario)
            db.session.commit()
        except:
            flash('Operation not commited in database')

        return redirect('/moderate')
    
    return render_template('moderate_number.html', form=form, usuario=usuario)
