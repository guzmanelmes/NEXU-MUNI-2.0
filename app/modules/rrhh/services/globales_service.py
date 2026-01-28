# app/modules/rrhh/services/globales_service.py
from app.extensions import db
from datetime import datetime
from app.modules.rrhh.models.globales import (
    Banco, AFP, Salud, Estamento, Feriado, 
    Sexo, NivelEstudio, Autoridad, TipoHaber
)

# --- BANCOS ---
def crear_banco(nombre):
    try:
        db.session.add(Banco(nombre=nombre))
        db.session.commit()
        return True, f'Banco "{nombre}" creado.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def obtener_bancos():
    return Banco.query.order_by(Banco.nombre).all()

def obtener_banco_por_id(id):
    return Banco.query.get(id)

def actualizar_banco(id, nombre):
    try:
        b = Banco.query.get(id)
        if b:
            b.nombre = nombre
            db.session.commit()
            return True, 'Banco actualizado.'
        return False, 'No encontrado.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def eliminar_banco(id):
    try:
        b = Banco.query.get(id)
        if b:
            db.session.delete(b)
            db.session.commit()
            return True, 'Banco eliminado.'
        return False, 'No encontrado.'
    except Exception as e:
        db.session.rollback()
        return False, 'No se puede eliminar: Registro en uso.'

# --- AFP ---
def crear_afp(nombre, tasa):
    try:
        db.session.add(AFP(nombre=nombre, tasa=tasa))
        db.session.commit()
        return True, f'AFP "{nombre}" creada.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def obtener_afps():
    return AFP.query.order_by(AFP.nombre).all()

def obtener_afp_por_id(id):
    return AFP.query.get(id)

def actualizar_afp(id, nombre, tasa):
    try:
        afp = AFP.query.get(id)
        if afp:
            afp.nombre = nombre
            afp.tasa = tasa
            db.session.commit()
            return True, 'AFP actualizada.'
        return False, 'No encontrada.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def eliminar_afp(id):
    try:
        afp = AFP.query.get(id)
        if afp:
            db.session.delete(afp)
            db.session.commit()
            return True, 'AFP eliminada.'
        return False, 'No encontrada.'
    except Exception as e:
        db.session.rollback()
        return False, 'No se puede eliminar: Registro en uso.'

# --- SALUD ---
def crear_salud(nombre, tipo):
    try:
        db.session.add(Salud(nombre=nombre, tipo=tipo))
        db.session.commit()
        return True, f'Institución "{nombre}" creada.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def obtener_salud():
    return Salud.query.order_by(Salud.nombre).all()

def obtener_salud_por_id(id):
    return Salud.query.get(id)

def actualizar_salud(id, nombre, tipo):
    try:
        s = Salud.query.get(id)
        if s:
            s.nombre = nombre
            s.tipo = tipo
            db.session.commit()
            return True, 'Institución actualizada.'
        return False, 'No encontrada.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def eliminar_salud(id):
    try:
        s = Salud.query.get(id)
        if s:
            db.session.delete(s)
            db.session.commit()
            return True, 'Institución eliminada.'
        return False, 'No encontrada.'
    except Exception as e:
        db.session.rollback()
        return False, 'Registro en uso.'

# --- ESTAMENTOS ---
def crear_estamento(nombre, g_min, g_max):
    try:
        if int(g_max) < int(g_min): return False, 'Grado Máx < Mín.'
        db.session.add(Estamento(estamento=nombre, grado_min=g_min, grado_max=g_max))
        db.session.commit()
        return True, 'Estamento creado.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def obtener_estamentos():
    return Estamento.query.order_by(Estamento.estamento).all()

def actualizar_estamento(id, nombre, g_min, g_max):
    try:
        e = Estamento.query.get(id)
        if e:
            e.estamento = nombre
            e.grado_min = g_min
            e.grado_max = g_max
            db.session.commit()
            return True, 'Estamento actualizado.'
        return False, 'No encontrado.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def eliminar_estamento(id):
    try:
        e = Estamento.query.get(id)
        if e:
            db.session.delete(e)
            db.session.commit()
            return True, 'Estamento eliminado.'
        return False, 'No encontrado.'
    except Exception as e:
        db.session.rollback()
        return False, 'Registro en uso.'

# --- FERIADOS ---
def crear_feriado(fecha_str, descripcion, es_irrenunciable):
    try:
        fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        if Feriado.query.filter_by(fecha=fecha_obj).first():
            return False, 'Ya existe feriado en esa fecha.'
        
        db.session.add(Feriado(fecha=fecha_obj, descripcion=descripcion, irrenunciable=(es_irrenunciable == 'on')))
        db.session.commit()
        return True, 'Feriado agregado.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def obtener_feriados():
    return Feriado.query.order_by(Feriado.fecha.desc()).all()

def eliminar_feriado(id):
    try:
        f = Feriado.query.get(id)
        if f:
            db.session.delete(f)
            db.session.commit()
            return True, 'Feriado eliminado.'
        return False, 'No encontrado.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

# --- AUTORIDADES ---
def crear_autoridad(nombre, cargo, decreto, rut=None):
    try:
        # Mapeamos 'nombre' del form al campo 'nombre' del modelo (firma_linea_1)
        db.session.add(Autoridad(nombre=nombre, cargo=cargo, decreto_nombramiento=decreto, rut=rut))
        db.session.commit()
        return True, 'Autoridad registrada.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def obtener_autoridades():
    return Autoridad.query.all()

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

# --- CATÁLOGOS SIMPLES (SEXO, ESTUDIOS, HABERES) ---
def obtener_generos():
    return Sexo.query.all()

def crear_genero(nombre):
    try:
        # OJO: Usamos 'descripcion' según tu DB
        db.session.add(Sexo(descripcion=nombre)) 
        db.session.commit()
        return True, 'Género/Sexo agregado'
    except:
        db.session.rollback()
        return False, 'Error al guardar'

def obtener_niveles_estudio():
    return NivelEstudio.query.all()

def crear_nivel_estudio(nombre):
    try:
        # OJO: Usamos 'descripcion' según tu DB
        db.session.add(NivelEstudio(descripcion=nombre))
        db.session.commit()
        return True, 'Nivel agregado'
    except:
        db.session.rollback()
        return False, 'Error al guardar'

def obtener_tipos_haberes():
    return TipoHaber.query.order_by(TipoHaber.codigo).all()

def crear_tipo_haber(codigo, descripcion, imponible, tributable):
    try:
        # OJO: Usamos 'nombre' según tu DB para la descripción
        nuevo = TipoHaber(
            codigo=codigo, 
            nombre=descripcion, 
            es_imponible=imponible,
            es_tributable=tributable
        )
        db.session.add(nuevo)
        db.session.commit()
        return True, 'Haber creado.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)