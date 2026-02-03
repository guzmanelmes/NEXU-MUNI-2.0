# app/modules/rrhh/services/funcionarios_service.py
from app.extensions import db
from app.modules.rrhh.models.funcionarios import Persona, PersonaArchivo

def actualizar_foto_perfil(funcionario, filename):
    try:
        funcionario.foto_perfil = filename
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False

def guardar_documento_digital(rut, nombre_visible, filename):
    try:
        nuevo_doc = PersonaArchivo(
            rut_persona=rut,
            nombre_visible=nombre_visible,
            nombre_archivo=filename,
            tipo_documento='CARPETA_DIGITAL'
        )
        db.session.add(nuevo_doc)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False

# --- NUEVA FUNCIÓN AGREGADA ---
def buscar_persona_por_rut(rut):
    """Busca una persona por su RUT exacto."""
    # Filtramos por el RUT tal cual viene (con puntos y guión si así se guarda)
    return Persona.query.filter_by(rut=rut).first()