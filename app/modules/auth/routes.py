from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.modules.auth.models import Usuario

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Si ya está logueado, lo mandamos al inicio
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = Usuario.query.filter_by(username=username).first()

        # Verificación de Seguridad
        if not user or not user.check_password(password):
            flash('Usuario o contraseña incorrectos', 'error')
            return redirect(url_for('auth.login'))
        
        if not user.activo:
            flash('Su cuenta está desactivada. Contacte al Administrador.', 'warning')
            return redirect(url_for('auth.login'))

        # Login exitoso
        login_user(user, remember=remember)
        
        # Redirección inteligente (si intentó entrar a una pag protegida)
        next_page = request.args.get('next')
        return redirect(next_page or url_for('core.dashboard'))

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ha cerrado sesión correctamente.', 'info')
    return redirect(url_for('auth.login'))