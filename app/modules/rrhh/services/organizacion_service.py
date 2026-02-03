from app.extensions import db
from app.modules.rrhh.models.organizacion import Unidad
from app.modules.rrhh.models.globales import Autoridad 

# =======================================================
# 1. GESTIÓN DE UNIDADES (Deptos, Direcciones)
# =======================================================

def obtener_unidades():
    return Unidad.query.order_by(Unidad.tipo, Unidad.nombre).all()

def obtener_unidad_por_id(id):
    return Unidad.query.get(id)

def crear_unidad(nombre, codigo, tipo, padre_id=None):
    try:
        if padre_id == '': padre_id = None
        
        nuevo = Unidad(
            nombre=nombre, 
            sigla=codigo, 
            tipo=tipo,
            padre_id=padre_id
        )
        db.session.add(nuevo)
        db.session.commit()
        return True, f'Unidad "{nombre}" creada.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def actualizar_unidad(id, nombre, codigo, tipo, padre_id=None):
    try:
        u = Unidad.query.get(id)
        if not u: return False, 'Unidad no encontrada.'

        if padre_id == '': padre_id = None
        
        # Validar ciclo (una unidad no puede ser padre de sí misma)
        if padre_id and int(padre_id) == int(id):
            return False, 'Error: Una unidad no puede depender de sí misma.'

        u.nombre = nombre
        u.sigla = codigo
        u.tipo = tipo
        u.padre_id = padre_id
        
        db.session.commit()
        return True, 'Unidad actualizada correctamente.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def eliminar_unidad(id):
    try:
        unidad = Unidad.query.get(id)
        if unidad:
            if unidad.sub_unidades.count() > 0:
                return False, 'No se puede eliminar: Tiene dependencias asignadas.'
            
            db.session.delete(unidad)
            db.session.commit()
            return True, 'Unidad eliminada.'
        return False, 'Unidad no encontrada.'
    except Exception as e:
        db.session.rollback()
        return False, 'Error al eliminar (tiene registros vinculados).'


# =======================================================
# 2. GESTIÓN DE AUTORIDADES (Firmantes)
# =======================================================

def obtener_autoridades():
    return Autoridad.query.all()

def obtener_autoridad_por_id(id):
    return Autoridad.query.get(id)

def crear_autoridad(rut, decreto, l1, l2, l3, l4, es_subrogante):
    try:
        nueva = Autoridad(
            rut=rut,
            decreto_nombramiento=decreto,
            firma_linea_1=l1,
            firma_linea_2=l2,
            firma_linea_3=l3,
            firma_linea_4=l4,
            es_subrogante=es_subrogante
        )
        db.session.add(nueva)
        db.session.commit()
        return True, 'Autoridad creada.'
    except Exception as e:
        db.session.rollback()
        return False, f'Error BD: {str(e)}'

def actualizar_autoridad(id, rut, decreto, l1, l2, l3, l4, es_subrogante):
    try:
        a = Autoridad.query.get(id)
        if not a: return False, 'Autoridad no encontrada.'

        a.rut = rut
        a.decreto_nombramiento = decreto
        a.firma_linea_1 = l1
        a.firma_linea_2 = l2
        a.firma_linea_3 = l3
        a.firma_linea_4 = l4
        a.es_subrogante = es_subrogante
        
        db.session.commit()
        return True, 'Autoridad actualizada correctamente.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def eliminar_autoridad(id):
    try:
        a = Autoridad.query.get(id)
        if a:
            db.session.delete(a)
            db.session.commit()
            return True, 'Autoridad eliminada.'
        return False, 'No encontrada.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)