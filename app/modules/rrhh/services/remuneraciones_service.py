from app.extensions import db
from app.modules.rrhh.models.globales import TipoHaber

# --- GESTIÓN DE HABERES Y FÓRMULAS ---
def obtener_tipos_haberes():
    return TipoHaber.query.order_by(TipoHaber.codigo).all()

def obtener_tipo_haber_por_id(id):
    return TipoHaber.query.get(id)

def crear_tipo_haber(codigo, nombre, imponible, tributable, manual, formula, permanente, visible):
    try:
        if manual and not formula: formula = ''
            
        nuevo = TipoHaber(
            codigo=codigo.upper().replace(" ", "_"), 
            nombre=nombre,
            es_imponible=imponible,
            es_tributable=tributable,
            es_manual=manual,
            formula=formula,
            es_permanente=permanente,
            es_visible_matriz=visible
        )
        db.session.add(nuevo)
        db.session.commit()
        return True, f'Haber {codigo} creado.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def actualizar_tipo_haber(id, codigo, nombre, imponible, tributable, manual, formula, permanente, visible):
    try:
        h = TipoHaber.query.get(id)
        if not h: return False, 'Haber no encontrado.'

        if manual: formula = ''

        h.codigo = codigo.upper().replace(" ", "_")
        h.nombre = nombre
        h.es_imponible = imponible
        h.es_tributable = tributable
        h.es_manual = manual
        h.formula = formula
        h.es_permanente = permanente
        h.es_visible_matriz = visible
        
        db.session.commit()
        return True, f'Haber {codigo} actualizado.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def eliminar_tipo_haber(id):
    try:
        h = TipoHaber.query.get(id)
        if h:
            db.session.delete(h)
            db.session.commit()
            return True, 'Haber eliminado.'
        return False, 'No encontrado.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)