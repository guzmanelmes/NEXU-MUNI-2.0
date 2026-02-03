from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.modules.rrhh import services
from . import rrhh_bp

# =======================================================
# 1. UNIDADES (Departamentos y Jerarquía)
# =======================================================

@rrhh_bp.route('/mantenedores/unidades', methods=['GET', 'POST'])
@login_required
def mantenedor_unidades():
    if request.method == 'POST':
        # CREAR
        nombre = request.form.get('nombre')
        codigo = request.form.get('codigo')
        tipo = request.form.get('tipo')
        padre_id = request.form.get('padre_id')
        
        if nombre and tipo:
            exito, msg = services.crear_unidad(nombre, codigo, tipo, padre_id)
            flash(msg, 'success' if exito else 'error')
        else:
            flash('Nombre y Tipo son obligatorios', 'error')
            
        return redirect(url_for('rrhh.mantenedor_unidades'))

    # LISTAR
    return render_template('rrhh/mantenedores/unidades.html', unidades=services.obtener_unidades())

@rrhh_bp.route('/mantenedores/unidades/editar/<int:id>', methods=['POST'])
@login_required
def editar_unidad(id):
    # ACTUALIZAR
    nombre = request.form.get('nombre')
    codigo = request.form.get('codigo')
    tipo = request.form.get('tipo')
    padre_id = request.form.get('padre_id')

    if nombre and tipo:
        exito, msg = services.actualizar_unidad(id, nombre, codigo, tipo, padre_id)
        flash(msg, 'success' if exito else 'error')
    else:
        flash('Faltan datos obligatorios', 'error')
        
    return redirect(url_for('rrhh.mantenedor_unidades'))

@rrhh_bp.route('/mantenedores/unidades/eliminar/<int:id>')
@login_required
def eliminar_unidad(id):
    # ELIMINAR
    exito, msg = services.eliminar_unidad(id)
    flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.mantenedor_unidades'))


# =======================================================
# 2. AUTORIDADES FIRMANTES
# =======================================================

@rrhh_bp.route('/mantenedores/autoridades', methods=['GET', 'POST'])
@login_required
def mantenedor_autoridades():
    if request.method == 'POST':
        # CREAR
        rut = request.form.get('rut')
        decreto = request.form.get('decreto')
        l1 = request.form.get('firma_linea_1')
        l2 = request.form.get('firma_linea_2')
        l3 = request.form.get('firma_linea_3')
        l4 = request.form.get('firma_linea_4')
        es_sub = (request.form.get('es_subrogante') == 'on')
        
        if l1 and l2:
            exito, msg = services.crear_autoridad(rut, decreto, l1, l2, l3, l4, es_sub)
            flash(msg, 'success' if exito else 'error')
        else:
            flash('Nombre y Cargo son obligatorios.', 'error')
            
        return redirect(url_for('rrhh.mantenedor_autoridades'))

    # LISTAR
    return render_template('rrhh/mantenedores/autoridades.html', autoridades=services.obtener_autoridades())

@rrhh_bp.route('/mantenedores/autoridades/editar/<int:id>', methods=['POST'])
@login_required
def editar_autoridad(id):
    # ACTUALIZAR
    rut = request.form.get('rut')
    decreto = request.form.get('decreto')
    l1 = request.form.get('firma_linea_1')
    l2 = request.form.get('firma_linea_2')
    l3 = request.form.get('firma_linea_3')
    l4 = request.form.get('firma_linea_4')
    es_sub = (request.form.get('es_subrogante') == 'on')

    if l1 and l2:
        exito, msg = services.actualizar_autoridad(id, rut, decreto, l1, l2, l3, l4, es_sub)
        flash(msg, 'success' if exito else 'error')
    else:
        flash('Faltan datos obligatorios', 'error')
        
    return redirect(url_for('rrhh.mantenedor_autoridades'))

@rrhh_bp.route('/mantenedores/autoridades/eliminar/<int:id>')
@login_required
def eliminar_autoridad(id):
    # ELIMINAR
    exito, msg = services.eliminar_autoridad(id)
    flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.mantenedor_autoridades'))