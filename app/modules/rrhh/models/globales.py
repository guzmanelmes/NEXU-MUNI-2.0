from app.extensions import db

# --- FINANCIEROS Y PREVISIÓN ---
class Banco(db.Model):
    __tablename__ = 'cat_bancos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

class AFP(db.Model):
    __tablename__ = 'cat_afp'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    tasa = db.Column(db.Numeric(4,2), default=0.00)

class Salud(db.Model):
    __tablename__ = 'cat_salud'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(20), nullable=False) # FONASA / ISAPRE

# --- PARÁMETROS RRHH ---
class Estamento(db.Model):
    __tablename__ = 'cat_estamentos'
    id = db.Column(db.Integer, primary_key=True)
    estamento = db.Column(db.String(100), nullable=False)
    grado_min = db.Column(db.Integer)
    grado_max = db.Column(db.Integer)

class Feriado(db.Model):
    __tablename__ = 'he_calendario_especial' 
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, unique=True, nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    es_irrenunciable = db.Column(db.Boolean, default=False)
    
    # Campo nuevo para diferenciar feriados legales de días administrativos
    tipo_dia = db.Column(db.String(50), default='FERIADO') # 'FERIADO' o 'ADMINISTRATIVO_MUNI'

class TipoHaber(db.Model):
    __tablename__ = 'config_tipo_haberes'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(150), nullable=False)
    
    # Flags Financieros
    es_imponible = db.Column(db.Boolean, default=True)
    es_tributable = db.Column(db.Boolean, default=True)
    
    # Flags de Lógica
    es_manual = db.Column(db.Boolean, default=True)         # 1=Monto Fijo, 0=Fórmula
    formula = db.Column(db.String(255), nullable=True)      # La fórmula matemática
    es_permanente = db.Column(db.Boolean, default=True)     # Si se paga todos los meses
    es_visible_matriz = db.Column(db.Boolean, default=True) # Si sale en la liquidación

# --- DEMOGRÁFICOS Y CONFIG ---
class Sexo(db.Model):
    __tablename__ = 'cat_sexo'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50), nullable=False)

class NivelEstudio(db.Model):
    __tablename__ = 'cat_nivel_estudios'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50), nullable=False)

# --- CONFIGURACIÓN DE FIRMAS ---
class Autoridad(db.Model):
    __tablename__ = 'cfg_autoridades_firmantes'
    
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(12))
    
    # Mapeo exacto de las 4 líneas de firma
    firma_linea_1 = db.Column(db.String(150), nullable=False) # Nombre
    firma_linea_2 = db.Column(db.String(150), nullable=False) # Cargo
    firma_linea_3 = db.Column(db.String(150))                 # Extra 1 (Subrogancia)
    firma_linea_4 = db.Column(db.String(150))                 # Extra 2 (Municipalidad...)
    
    decreto_nombramiento = db.Column(db.String(100))
    es_subrogante = db.Column(db.Boolean, default=False)

# --- TIPOS DE CONTRATO ---
class TipoContrato(db.Model):
    __tablename__ = 'cfg_tipos_contrato'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    
    # Configuraciones Lógicas
    es_jornada_completa = db.Column(db.Boolean, default=False)  # 44 hrs vs parcial
    usa_asistencia = db.Column(db.Boolean, default=True)        # ¿Debe marcar reloj?
    plantilla_word = db.Column(db.String(100), default='honorario_estandar.docx')

# --- PROGRAMAS Y CUENTAS PRESUPUESTARIAS (CORREGIDO) ---
class Programa(db.Model):
    __tablename__ = 'programas'
    __table_args__ = {'extend_existing': True} # <--- SOLUCIÓN AL ERROR
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    numero_decreto = db.Column(db.String(50), nullable=False)
    fecha_decreto = db.Column(db.Date, nullable=False)
    archivo_adjunto = db.Column(db.String(255)) # PDF del decreto
    
    # Relación: Un Programa tiene muchas Cuentas
    cuentas = db.relationship('CuentaPresupuestaria', backref='programa', lazy=True, cascade="all, delete-orphan")

class CuentaPresupuestaria(db.Model):
    __tablename__ = 'cuentas_presupuestarias'
    __table_args__ = {'extend_existing': True} # <--- SOLUCIÓN AL ERROR
    
    id = db.Column(db.Integer, primary_key=True)
    programa_id = db.Column(db.Integer, db.ForeignKey('programas.id'), nullable=False)
    
    codigo = db.Column(db.String(50), nullable=False) # Ej: 215.21.04.004.001
    descripcion = db.Column(db.String(100))
    monto_inicial = db.Column(db.Integer, default=0)
    saldo_actual = db.Column(db.Integer, default=0)