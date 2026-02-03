from app.extensions import db
from datetime import datetime
from app.modules.rrhh.models.globales import Feriado

# --- LISTAR ---
def obtener_feriados():
    # Ordenamos por fecha descendente (lo más futuro primero)
    return Feriado.query.order_by(Feriado.fecha.desc()).all()

def obtener_feriado_por_id(id):
    return Feriado.query.get(id)

# --- CREAR ---
def crear_feriado(fecha_str, descripcion, es_irrenunciable, tipo_dia):
    try:
        fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        
        # Validar duplicados
        if Feriado.query.filter_by(fecha=fecha_obj).first():
            return False, 'Ya existe un evento configurado en esa fecha.'
        
        nuevo = Feriado(
            fecha=fecha_obj, 
            descripcion=descripcion, 
            es_irrenunciable=es_irrenunciable,
            tipo_dia=tipo_dia
        )
        db.session.add(nuevo)
        db.session.commit()
        return True, 'Día agregado.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

# --- ACTUALIZAR ---
def actualizar_feriado(id, fecha_str, descripcion, es_irrenunciable, tipo_dia):
    try:
        f = Feriado.query.get(id)
        if not f: return False, 'Registro no encontrado.'

        f.fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        f.descripcion = descripcion
        f.es_irrenunciable = es_irrenunciable
        f.tipo_dia = tipo_dia
        
        db.session.commit()
        return True, 'Registro actualizado.'
    except Exception as e:
        db.session.rollback()
        return False, f'Error al actualizar: {str(e)}'

# --- ELIMINAR ---
def eliminar_feriado(id):
    try:
        f = Feriado.query.get(id)
        if f:
            db.session.delete(f)
            db.session.commit()
            return True, 'Registro eliminado.'
        return False, 'No encontrado.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)