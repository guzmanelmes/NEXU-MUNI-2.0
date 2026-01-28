import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

# Importamos "services" que ahora es un PAQUETE (gracias al __init__.py que creamos)
# Esto nos da acceso a todas las funciones: services.crear_banco, services.crear_unidad, etc.
from app.modules.rrhh import services 

rrhh_bp = Blueprint('rrhh', __name__, url_prefix='/rrhh')

# Configuración de archivos permitidos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx', 'doc'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# =======================================================
# 1. FICHA DEL FUNCIONARIO (Mi Perfil)
# =======================================================

@rrhh_bp.route('/mi-ficha')
@login_required
def mi_ficha():
    # Obtiene el funcionario ligado al usuario actual
    funcionario = current_user.ficha_personal
    if not funcionario:
        return render_template('errores/no_vinculado.html') 
    return render_template('rrhh/ficha.html', p=funcionario)

@rrhh_bp.route('/subir-foto', methods=['POST'])
@login_required
def subir_foto():
    funcionario = current_user.ficha_personal
    file = request.files.get('foto')
    
    if not file or file.filename == '':
        flash('Debe seleccionar una imagen.', 'error')
        return redirect(url_for('rrhh.mi_ficha'))

    if allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{funcionario.rut}_perfil.{ext}"
        
        # Guardar en sistema de archivos
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'fotos')
        os.makedirs(upload_path, exist_ok=True)
        file.save(os.path.join(upload_path, filename))
        
        # Actualizar BD usando el servicio de funcionarios
        if services.actualizar_foto_perfil(funcionario, filename):
            flash('Foto actualizada.', 'success')
        else:
            flash('Error al guardar en base de datos.', 'error')
    else:
        flash('Formato no permitido.', 'error')

    return redirect(url_for('rrhh.mi_ficha'))

@rrhh_bp.route('/subir-documento', methods=['POST'])
@login_required
def subir_documento():
    funcionario = current_user.ficha_personal
    file = request.files.get('documento')
    nombre_visible = request.form.get('nombre_documento')
    
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{funcionario.rut}_{file.filename}")
        
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'documentos')
        os.makedirs(upload_path, exist_ok=True)
        file.save(os.path.join(upload_path, filename))
        
        if services.guardar_documento_digital(funcionario.rut, nombre_visible, filename):
            flash('Documento agregado.', 'success')
        else:
            flash('Error al registrar documento.', 'error')
    else:
        flash('Archivo inválido o error de carga.', 'error')
        
    return redirect(url_for('rrhh.mi_ficha'))


# =======================================================
# 2. MANTENEDORES GLOBALES (Bancos, AFP, Salud)
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

# --- SALUD (ISAPRE/FONASA) ---
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


# =======================================================
# 3. MANTENEDORES DE CONFIGURACIÓN (Estamentos, Feriados)
# =======================================================

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

# --- FERIADOS (Calendario) ---
@rrhh_bp.route('/mantenedores/feriados', methods=['GET', 'POST'])
@login_required
def mantenedor_feriados():
    if request.method == 'POST':
        fecha = request.form.get('fecha')
        descripcion = request.form.get('descripcion')
        irrenunciable = request.form.get('irrenunciable') 
        
        if fecha and descripcion:
            exito, msg = services.crear_feriado(fecha, descripcion, irrenunciable)
            flash(msg, 'success' if exito else 'error')
        else:
            flash('Fecha y descripción son obligatorios', 'error')
        return redirect(url_for('rrhh.mantenedor_feriados'))

    return render_template('rrhh/mantenedores/feriados.html', feriados=services.obtener_feriados())

@rrhh_bp.route('/mantenedores/feriados/eliminar/<int:id>')
@login_required
def eliminar_feriado(id):
    exito, msg = services.eliminar_feriado(id)
    flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.mantenedor_feriados'))


# =======================================================
# 4. NUEVOS MANTENEDORES (Organización y Parámetros)
# =======================================================

# --- UNIDADES (Departamentos) ---
@rrhh_bp.route('/mantenedores/unidades', methods=['GET', 'POST'])
@login_required
def mantenedor_unidades():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        codigo = request.form.get('codigo')
        if nombre:
            # Usamos el servicio de organización
            exito, msg = services.crear_unidad(nombre, codigo)
            flash(msg, 'success' if exito else 'error')
        return redirect(url_for('rrhh.mantenedor_unidades'))

    return render_template('rrhh/mantenedores/unidades.html', unidades=services.obtener_unidades())

@rrhh_bp.route('/mantenedores/unidades/eliminar/<int:id>')
@login_required
def eliminar_unidad(id):
    exito, msg = services.eliminar_unidad(id)
    flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.mantenedor_unidades'))

# --- AUTORIDADES FIRMANTES ---
@rrhh_bp.route('/mantenedores/autoridades', methods=['GET', 'POST'])
@login_required
def mantenedor_autoridades():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        cargo = request.form.get('cargo')
        decreto = request.form.get('decreto')
        rut = request.form.get('rut')
        
        if nombre and cargo:
            exito, msg = services.crear_autoridad(nombre, cargo, decreto, rut)
            flash(msg, 'success' if exito else 'error')
        return redirect(url_for('rrhh.mantenedor_autoridades'))

    return render_template('rrhh/mantenedores/autoridades.html', autoridades=services.obtener_autoridades())

@rrhh_bp.route('/mantenedores/autoridades/eliminar/<int:id>')
@login_required
def eliminar_autoridad(id):
    exito, msg = services.eliminar_autoridad(id)
    flash(msg, 'success' if exito else 'error')
    return redirect(url_for('rrhh.mantenedor_autoridades'))

# --- PARÁMETROS VARIOS (Géneros, Estudios, Haberes) ---
@rrhh_bp.route('/mantenedores/parametros', methods=['GET', 'POST'])
@login_required
def mantenedor_parametros():
    if request.method == 'POST':
        tipo = request.form.get('tipo_parametro')
        nombre = request.form.get('nombre') # Usado para géneros y estudios
        
        exito = False
        msg = "Error desconocido"

        if tipo == 'genero':
            exito, msg = services.crear_genero(nombre)
        
        elif tipo == 'estudio':
            exito, msg = services.crear_nivel_estudio(nombre)
        
        elif tipo == 'haber':
            exito, msg = services.crear_tipo_haber(
                codigo=request.form.get('codigo'),
                descripcion=request.form.get('descripcion'), # Se guardará como 'nombre' en DB
                imponible=(request.form.get('imponible') == 'on'),
                tributable=(request.form.get('tributable') == 'on')
            )
        
        flash(msg, 'success' if exito else 'error')
        return redirect(url_for('rrhh.mantenedor_parametros'))

    return render_template('rrhh/mantenedores/parametros.html', 
                           generos=services.obtener_generos(),
                           estudios=services.obtener_niveles_estudio(),
                           haberes=services.obtener_tipos_haberes())