# app/modules/rrhh/services/organizacion_service.py
from app.extensions import db
from app.modules.rrhh.models.organizacion import Unidad

def crear_unidad(nombre, codigo):
    try:
        # Por ahora creamos todo como 'DEPARTAMENTO' o genérico si no se especifica jerarquía compleja
        # Ajustado para usar los campos de tu modelo actual
        nuevo = Unidad(nombre=nombre, sigla=codigo, tipo='DEPARTAMENTO') 
        db.session.add(nuevo)
        db.session.commit()
        return True, f'Unidad "{nombre}" creada.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def obtener_unidades():
    return Unidad.query.order_by(Unidad.nombre).all()

def eliminar_unidad(id):
    try:
        unidad = Unidad.query.get(id)
        if unidad:
            db.session.delete(unidad)
            db.session.commit()
            return True, 'Unidad eliminada.'
        return False, 'Unidad no encontrada.'
    except Exception as e:
        db.session.rollback()
        return False, 'No se puede eliminar: Hay contratos en esta unidad.'