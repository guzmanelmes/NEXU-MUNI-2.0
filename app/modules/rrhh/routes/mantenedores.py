import os
from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from app.modules.rrhh import services
from . import rrhh_bp

# Configuración de archivos permitidos (Solo Word y PDF para decretos)
def allowed_file(filename):
    # Permitimos .doc, .docx y .pdf
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'docx', 'doc', 'pdf'}

# =======================================================
# MANTENEDORES GLOBALES
# =======================================================

# --- BANCOS ---
@rrhh_bp.route('/mantenedores/bancos', methods=['GET', 'POST'])
@login_required
def mantenedor_bancos():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        if nombre:
            exito, msg = services.crear_banco(nombre)
            flash(msg, 'success' if exito else 'error')
        return redirect(url_for('rrhh.mantenedor_bancos'))
    return render_template('rrhh/mantenedores/bancos.html', bancos=services.obtener_bancos())

@rrhh_bp.route('/mantenedores/bancos/editar/<int:id>', methods=['POST'])
@login_required
def editar_banco(id):
    nuevo_nombre = request.form.get('nombre')
    if nuevo_nombre:
        exito, msg = services.actualizar_banco(id, nuevo_nombre)
        flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.mantenedor_bancos'))

@rrhh_bp.route('/mantenedores/bancos/eliminar/<int:id>')
@login_required
def eliminar_banco(id):
    exito, msg = services.eliminar_banco(id)
    flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.mantenedor_bancos'))

# --- AFP ---
@rrhh_bp.route('/mantenedores/afp', methods=['GET', 'POST'])
@login_required
def mantenedor_afp():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        tasa = request.form.get('tasa') or 0
        if nombre:
            exito, msg = services.crear_afp(nombre, tasa)
            flash(msg, 'success' if exito else 'error')
        return redirect(url_for('rrhh.mantenedor_afp'))
    return render_template('rrhh/mantenedores/afp.html', afps=services.obtener_afps())

@rrhh_bp.route('/mantenedores/afp/editar/<int:id>', methods=['POST'])
@login_required
def editar_afp(id):
    nombre = request.form.get('nombre')
    tasa = request.form.get('tasa')
    if nombre:
        exito, msg = services.actualizar_afp(id, nombre, tasa)
        flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.mantenedor_afp'))

@rrhh_bp.route('/mantenedores/afp/eliminar/<int:id>')
@login_required
def eliminar_afp(id):
    exito, msg = services.eliminar_afp(id)
    flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.mantenedor_afp'))

# --- SALUD ---
@rrhh_bp.route('/mantenedores/salud', methods=['GET', 'POST'])
@login_required
def mantenedor_salud():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        tipo = request.form.get('tipo')
        if nombre and tipo:
            exito, msg = services.crear_salud(nombre, tipo)
            flash(msg, 'success' if exito else 'error')
        return redirect(url_for('rrhh.mantenedor_salud'))
    return render_template('rrhh/mantenedores/salud.html', instituciones=services.obtener_salud())

@rrhh_bp.route('/mantenedores/salud/editar/<int:id>', methods=['POST'])
@login_required
def editar_salud(id):
    nombre = request.form.get('nombre')
    tipo = request.form.get('tipo')
    if nombre and tipo:
        exito, msg = services.actualizar_salud(id, nombre, tipo)
        flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.mantenedor_salud'))

@rrhh_bp.route('/mantenedores/salud/eliminar/<int:id>')
@login_required
def eliminar_salud(id):
    exito, msg = services.eliminar_salud(id)
    flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.mantenedor_salud'))

# --- ESTAMENTOS ---
@rrhh_bp.route('/mantenedores/estamentos', methods=['GET', 'POST'])
@login_required
def mantenedor_estamentos():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        g_min = request.form.get('grado_min')
        g_max = request.form.get('grado_max')
        if nombre and g_min and g_max:
            exito, msg = services.crear_estamento(nombre, g_min, g_max)
            flash(msg, 'success' if exito else 'error')
        else:
            flash('Todos los campos son obligatorios', 'error')
        return redirect(url_for('rrhh.mantenedor_estamentos'))
    return render_template('rrhh/mantenedores/estamentos.html', estamentos=services.obtener_estamentos())

@rrhh_bp.route('/mantenedores/estamentos/editar/<int:id>', methods=['POST'])
@login_required
def editar_estamento(id):
    nombre = request.form.get('nombre')
    g_min = request.form.get('grado_min')
    g_max = request.form.get('grado_max')
    if nombre:
        exito, msg = services.actualizar_estamento(id, nombre, g_min, g_max)
        flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.mantenedor_estamentos'))

@rrhh_bp.route('/mantenedores/estamentos/eliminar/<int:id>')
@login_required
def eliminar_estamento(id):
    exito, msg = services.eliminar_estamento(id)
    flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.mantenedor_estamentos'))

# =======================================================
# PARÁMETROS: HABERES, GÉNEROS, ESTUDIOS Y CONTRATOS
# =======================================================

@rrhh_bp.route('/mantenedores/parametros', methods=['GET', 'POST'])
@login_required
def mantenedor_parametros():
    if request.method == 'POST':
        tipo = request.form.get('tipo_parametro')
        nombre = request.form.get('nombre') 
        
        exito = False
        msg = "Error desconocido"

        if tipo == 'genero':
            exito, msg = services.crear_genero(nombre)
        
        elif tipo == 'estudio':
            exito, msg = services.crear_nivel_estudio(nombre)
        
        elif tipo == 'haber':
            es_manual = (request.form.get('es_manual') == 'on')
            exito, msg = services.crear_tipo_haber(
                codigo=request.form.get('codigo'),
                nombre=request.form.get('descripcion'), 
                imponible=(request.form.get('imponible') == 'on'),
                tributable=(request.form.get('tributable') == 'on'),
                manual=es_manual,
                formula=request.form.get('formula'),
                permanente=(request.form.get('es_permanente') == 'on'),
                visible=(request.form.get('es_visible_matriz') == 'on')
            )
        
        elif tipo == 'contrato':
            # 1. Manejo del Archivo
            archivo = request.files.get('plantilla_file')
            filename = 'honorario_estandar.docx' # Default
            
            if archivo and archivo.filename != '' and allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                upload_path = os.path.join(current_app.root_path, 'static', 'plantillas')
                os.makedirs(upload_path, exist_ok=True)
                archivo.save(os.path.join(upload_path, filename))
            
            # 2. Guardar en BD
            exito, msg = services.crear_tipo_contrato(
                nombre=request.form.get('nombre'),
                jornada_completa=(request.form.get('es_jornada_completa') == 'on'),
                usa_asistencia=(request.form.get('usa_asistencia') == 'on'),
                plantilla=filename
            )
        
        flash(msg, 'success' if exito else 'error')
        return redirect(url_for('rrhh.mantenedor_parametros'))

    return render_template('rrhh/mantenedores/parametros.html', 
                           generos=services.obtener_generos(),
                           estudios=services.obtener_niveles_estudio(),
                           haberes=services.obtener_tipos_haberes(),
                           contratos=services.obtener_tipos_contrato())

# --- HABERES ---
@rrhh_bp.route('/mantenedores/haberes/editar/<int:id>', methods=['POST'])
@login_required
def editar_haber(id):
    es_manual = (request.form.get('es_manual') == 'on')
    exito, msg = services.actualizar_tipo_haber(
        id=id,
        codigo=request.form.get('codigo'),
        nombre=request.form.get('descripcion'), 
        imponible=(request.form.get('imponible') == 'on'),
        tributable=(request.form.get('tributable') == 'on'),
        manual=es_manual,
        formula=request.form.get('formula'),
        permanente=(request.form.get('es_permanente') == 'on'),
        visible=(request.form.get('es_visible_matriz') == 'on')
    )
    flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.mantenedor_parametros'))

@rrhh_bp.route('/mantenedores/haberes/eliminar/<int:id>')
@login_required
def eliminar_haber(id):
    exito, msg = services.eliminar_tipo_haber(id)
    flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.mantenedor_parametros'))

# --- GÉNEROS ---
@rrhh_bp.route('/mantenedores/generos/editar/<int:id>', methods=['POST'])
@login_required
def editar_genero(id):
    nombre = request.form.get('nombre')
    if nombre:
        exito, msg = services.actualizar_genero(id, nombre)
        flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.mantenedor_parametros'))

@rrhh_bp.route('/mantenedores/generos/eliminar/<int:id>')
@login_required
def eliminar_genero(id):
    exito, msg = services.eliminar_genero(id)
    flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.mantenedor_parametros'))

# --- ESTUDIOS ---
@rrhh_bp.route('/mantenedores/estudios/editar/<int:id>', methods=['POST'])
@login_required
def editar_estudio(id):
    nombre = request.form.get('nombre')
    if nombre:
        exito, msg = services.actualizar_nivel_estudio(id, nombre)
        flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.mantenedor_parametros'))

@rrhh_bp.route('/mantenedores/estudios/eliminar/<int:id>')
@login_required
def eliminar_estudio(id):
    exito, msg = services.eliminar_nivel_estudio(id)
    flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.mantenedor_parametros'))

# --- TIPOS DE CONTRATO ---
@rrhh_bp.route('/mantenedores/contratos/editar/<int:id>', methods=['POST'])
@login_required
def editar_contrato(id):
    archivo = request.files.get('plantilla_file')
    filename = None
    if archivo and archivo.filename != '' and allowed_file(archivo.filename):
        filename = secure_filename(archivo.filename)
        upload_path = os.path.join(current_app.root_path, 'static', 'plantillas')
        os.makedirs(upload_path, exist_ok=True)
        archivo.save(os.path.join(upload_path, filename))

    exito, msg = services.actualizar_tipo_contrato(
        id=id,
        nombre=request.form.get('nombre'),
        jornada_completa=(request.form.get('es_jornada_completa') == 'on'),
        usa_asistencia=(request.form.get('usa_asistencia') == 'on'),
        plantilla=filename
    )
    flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.mantenedor_parametros'))

@rrhh_bp.route('/mantenedores/contratos/eliminar/<int:id>')
@login_required
def eliminar_contrato(id):
    exito, msg = services.eliminar_tipo_contrato(id)
    flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.mantenedor_parametros'))

# =======================================================
# NUEVO MÓDULO: GESTIÓN DE PROGRAMAS (Rutas dedicadas)
# =======================================================

@rrhh_bp.route('/programas', methods=['GET', 'POST'])
@login_required
def gestion_programas():
    # 1. CREACIÓN (POST)
    if request.method == 'POST':
        archivo = request.files.get('archivo_decreto')
        filename = None
        if archivo and archivo.filename != '':
            filename = secure_filename(archivo.filename)
            path = os.path.join(current_app.root_path, 'static', 'uploads', 'decretos')
            os.makedirs(path, exist_ok=True)
            archivo.save(os.path.join(path, filename))

        exito, msg = services.crear_programa(
            nombre=request.form.get('nombre'),
            n_decreto=request.form.get('numero_decreto'),
            f_decreto=request.form.get('fecha_decreto'),
            archivo=filename
        )
        flash(msg, 'success' if exito else 'error')
        return redirect(url_for('rrhh.gestion_programas'))

    # 2. LISTADO (GET)
    return render_template('rrhh/programas.html', programas=services.obtener_programas())

@rrhh_bp.route('/programas/editar/<int:id>', methods=['POST'])
@login_required
def editar_programa(id):
    archivo = request.files.get('archivo_decreto')
    filename = None
    if archivo and archivo.filename != '':
        filename = secure_filename(archivo.filename)
        path = os.path.join(current_app.root_path, 'static', 'uploads', 'decretos')
        os.makedirs(path, exist_ok=True)
        archivo.save(os.path.join(path, filename))

    exito, msg = services.actualizar_programa(
        id=id,
        nombre=request.form.get('nombre'),
        n_decreto=request.form.get('numero_decreto'),
        f_decreto=request.form.get('fecha_decreto'),
        archivo=filename
    )
    flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.gestion_programas'))

@rrhh_bp.route('/programas/eliminar/<int:id>')
@login_required
def eliminar_programa(id):
    exito, msg = services.eliminar_programa(id)
    flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.gestion_programas'))

# --- CUENTAS PRESUPUESTARIAS ---
@rrhh_bp.route('/programas/agregar_cuenta', methods=['POST'])
@login_required
def agregar_cuenta_presupuestaria():
    prog_id = request.form.get('programa_id')
    codigo = request.form.get('codigo')
    desc = request.form.get('descripcion')
    monto = request.form.get('monto_inicial')
    
    if prog_id and codigo:
        exito, msg = services.agregar_cuenta_presupuestaria(prog_id, codigo, desc, monto)
        flash(msg, 'success' if exito else 'error')
    else:
        flash('Faltan datos para la cuenta', 'error')
        
    return redirect(url_for('rrhh.gestion_programas'))

@rrhh_bp.route('/programas/eliminar_cuenta/<int:id>')
@login_required
def eliminar_cuenta_presupuestaria(id):
    exito, msg = services.eliminar_cuenta_presupuestaria(id)
    flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.gestion_programas'))