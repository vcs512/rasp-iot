from crypt import methods
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response

from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from . import main
from .forms import TrocaRole, ExcluirUser
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


# about project
@main.route('/project_info',methods=['POST','GET'])
def project_info():
    return render_template('project_info.html')



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
        
        try:
            usuario.role_id = role
            db.session.add(usuario)
            db.session.commit()
        except:
            flash('Operation not commited in database')

        return redirect('/moderate')
    
    return render_template('moderate_number.html', form=form, usuario=usuario)


# exclude user page
@main.route('/exclude/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADMIN)
def exclude_number(id):
    form = ExcluirUser()
    usuario = User.query.get_or_404(id)
    print(usuario)

    # if ADMIN scapes
    if usuario.role_id == 3:
        return redirect('/moderate')
    
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):

            try:
                db.session.delete(usuario)
                db.session.commit()
                flash('User excluded')
            except:
                flash('Operation not commited in database')

            return redirect('/moderate')
    
    return render_template('exclude_number.html', form=form, usuario=usuario)    
