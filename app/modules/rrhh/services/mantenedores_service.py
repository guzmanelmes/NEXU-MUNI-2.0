from app.extensions import db
from app.modules.rrhh.models.globales import Banco, AFP, Salud, Sexo, NivelEstudio, Estamento, TipoContrato, Programa, CuentaPresupuestaria
from datetime import datetime

# =======================================================
# 1. BANCOS
# =======================================================
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

# =======================================================
# 2. AFP
# =======================================================
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

# =======================================================
# 3. SALUD (ISAPRE/FONASA)
# =======================================================
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

# =======================================================
# 4. CATÁLOGOS SIMPLES: GÉNERO
# =======================================================
def obtener_generos():
    return Sexo.query.order_by(Sexo.descripcion).all()

def obtener_genero_por_id(id):
    return Sexo.query.get(id)

def crear_genero(nombre):
    try:
        db.session.add(Sexo(descripcion=nombre)) 
        db.session.commit()
        return True, 'Género agregado.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def actualizar_genero(id, nombre):
    try:
        g = Sexo.query.get(id)
        if not g: return False, 'Género no encontrado.'
        
        g.descripcion = nombre
        db.session.commit()
        return True, 'Género actualizado.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def eliminar_genero(id):
    try:
        g = Sexo.query.get(id)
        if g:
            db.session.delete(g)
            db.session.commit()
            return True, 'Género eliminado.'
        return False, 'No encontrado.'
    except Exception as e:
        db.session.rollback()
        return False, 'Error al eliminar (Probablemente en uso).'

# =======================================================
# 5. CATÁLOGOS SIMPLES: NIVELES DE ESTUDIO
# =======================================================
def obtener_niveles_estudio():
    return NivelEstudio.query.order_by(NivelEstudio.descripcion).all()

def obtener_nivel_estudio_por_id(id):
    return NivelEstudio.query.get(id)

def crear_nivel_estudio(nombre):
    try:
        db.session.add(NivelEstudio(descripcion=nombre))
        db.session.commit()
        return True, 'Nivel agregado.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def actualizar_nivel_estudio(id, nombre):
    try:
        n = NivelEstudio.query.get(id)
        if not n: return False, 'Nivel no encontrado.'
        
        n.descripcion = nombre
        db.session.commit()
        return True, 'Nivel actualizado.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def eliminar_nivel_estudio(id):
    try:
        n = NivelEstudio.query.get(id)
        if n:
            db.session.delete(n)
            db.session.commit()
            return True, 'Nivel eliminado.'
        return False, 'No encontrado.'
    except Exception as e:
        db.session.rollback()
        return False, 'Error al eliminar (Probablemente en uso).'

# =======================================================
# 6. ESTAMENTOS
# =======================================================
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

# =======================================================
# 7. TIPOS DE CONTRATO (CRUD COMPLETO)
# =======================================================
def obtener_tipos_contrato():
    return TipoContrato.query.order_by(TipoContrato.nombre).all()

def obtener_tipo_contrato_por_id(id):
    return TipoContrato.query.get(id)

def crear_tipo_contrato(nombre, jornada_completa, usa_asistencia, plantilla):
    try:
        if not plantilla: plantilla = 'honorario_estandar.docx'
        
        nuevo = TipoContrato(
            nombre=nombre,
            es_jornada_completa=jornada_completa,
            usa_asistencia=usa_asistencia,
            plantilla_word=plantilla
        )
        db.session.add(nuevo)
        db.session.commit()
        return True, 'Tipo de Contrato configurado.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def actualizar_tipo_contrato(id, nombre, jornada_completa, usa_asistencia, plantilla=None):
    try:
        c = TipoContrato.query.get(id)
        if not c: return False, 'No encontrado.'
        
        c.nombre = nombre
        c.es_jornada_completa = jornada_completa
        c.usa_asistencia = usa_asistencia
        
        # Solo actualizamos la plantilla si se subió un archivo nuevo
        if plantilla:
            c.plantilla_word = plantilla
        
        db.session.commit()
        return True, 'Configuración actualizada.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def eliminar_tipo_contrato(id):
    try:
        c = TipoContrato.query.get(id)
        if c:
            db.session.delete(c)
            db.session.commit()
            return True, 'Tipo eliminado.'
        return False, 'No encontrado.'
    except Exception as e:
        db.session.rollback()
        return False, 'Error: Está asignado a contratos vigentes.'

# =======================================================
# 8. PROGRAMAS Y CUENTAS (Lógica Real)
# =======================================================
def obtener_programas():
    return Programa.query.order_by(Programa.nombre).all()

# --- GESTIÓN DEL PROGRAMA (PADRE) ---
def crear_programa(nombre, n_decreto, f_decreto, archivo=None):
    try:
        # Convertir fecha string -> date
        fecha_obj = datetime.strptime(f_decreto, '%Y-%m-%d').date()
        
        nuevo = Programa(
            nombre=nombre, 
            numero_decreto=n_decreto, 
            fecha_decreto=fecha_obj,
            archivo_adjunto=archivo
        )
        db.session.add(nuevo)
        db.session.commit()
        return True, 'Programa creado correctamente.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def actualizar_programa(id, nombre, n_decreto, f_decreto, archivo=None):
    try:
        p = Programa.query.get(id)
        if not p: return False, 'No encontrado.'
        
        p.nombre = nombre
        p.numero_decreto = n_decreto
        if f_decreto:
            p.fecha_decreto = datetime.strptime(f_decreto, '%Y-%m-%d').date()
        
        if archivo: # Solo actualizamos si suben uno nuevo
            p.archivo_adjunto = archivo
            
        db.session.commit()
        return True, 'Programa actualizado.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def eliminar_programa(id):
    try:
        p = Programa.query.get(id)
        if p:
            db.session.delete(p)
            db.session.commit()
            return True, 'Programa eliminado.'
        return False, 'No encontrado.'
    except Exception as e:
        db.session.rollback()
        return False, 'Error: Tiene movimientos asociados.'

# --- GESTIÓN DE CUENTAS (HIJOS) ---
def agregar_cuenta_presupuestaria(programa_id, codigo, descripcion, monto):
    try:
        monto_int = int(monto) if monto else 0
        nueva = CuentaPresupuestaria(
            programa_id=programa_id,
            codigo=codigo,
            descripcion=descripcion,
            monto_inicial=monto_int,
            saldo_actual=monto_int # Saldo inicial = Monto inicial
        )
        db.session.add(nueva)
        db.session.commit()
        return True, 'Cuenta agregada.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def eliminar_cuenta_presupuestaria(cuenta_id):
    try:
        c = CuentaPresupuestaria.query.get(cuenta_id)
        if c:
            db.session.delete(c)
            db.session.commit()
            return True, 'Cuenta eliminada.'
        return False, 'No encontrada.'
    except Exception as e:
        db.session.rollback()
        return False, str(e)