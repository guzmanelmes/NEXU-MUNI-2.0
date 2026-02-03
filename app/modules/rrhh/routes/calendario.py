from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.modules.rrhh import services
from . import rrhh_bp

# --- FERIADOS (Calendario) ---
@rrhh_bp.route('/mantenedores/feriados', methods=['GET', 'POST'])
@login_required
def mantenedor_feriados():
    if request.method == 'POST':
        fecha = request.form.get('fecha')
        descripcion = request.form.get('descripcion')
        tipo_dia = request.form.get('tipo_dia')
        irrenunciable = (request.form.get('irrenunciable') == 'on')
        
        if fecha and descripcion:
            exito, msg = services.crear_feriado(fecha, descripcion, irrenunciable, tipo_dia)
            flash(msg, 'success' if exito else 'error')
        else:
            flash('Fecha y descripción son obligatorios', 'error')
        return redirect(url_for('rrhh.mantenedor_feriados'))

    return render_template('rrhh/mantenedores/feriados.html', feriados=services.obtener_feriados())

@rrhh_bp.route('/mantenedores/feriados/editar/<int:id>', methods=['POST'])
@login_required
def editar_feriado(id):
    fecha = request.form.get('fecha')
    descripcion = request.form.get('descripcion')
    tipo_dia = request.form.get('tipo_dia')
    irrenunciable = (request.form.get('irrenunciable') == 'on')

    if fecha and descripcion:
        exito, msg = services.actualizar_feriado(id, fecha, descripcion, irrenunciable, tipo_dia)
        flash(msg, 'success' if exito else 'error')
    else:
        flash('Faltan datos obligatorios', 'error')
        
    return redirect(url_for('rrhh.mantenedor_feriados'))

@rrhh_bp.route('/mantenedores/feriados/eliminar/<int:id>')
@login_required
def eliminar_feriado(id):
    exito, msg = services.eliminar_feriado(id)
    flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.mantenedor_feriados'))