import os
from flask import render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.modules.rrhh import services
from . import rrhh_bp # Importamos el Blueprint del __init__

# Configuración de archivos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx', 'doc'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# =======================================================
# 1. FICHA DEL FUNCIONARIO (Mi Perfil)
# =======================================================

@rrhh_bp.route('/mi-ficha')
@login_required
def mi_ficha():
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
        
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'fotos')
        os.makedirs(upload_path, exist_ok=True)
        file.save(os.path.join(upload_path, filename))
        
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
# API INTERNA
# =======================================================

@rrhh_bp.route('/api/buscar_persona/<path:rut>')
@login_required
def api_buscar_persona(rut):
    persona = services.buscar_persona_por_rut(rut)
    if persona:
        return jsonify({
            'encontrado': True,
            'nombre_completo': persona.nombre_completo,
            'rut': persona.rut
        })
    else:
        return jsonify({'encontrado': False})