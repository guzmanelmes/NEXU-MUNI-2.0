# app/modules/rrhh/models/globales.py
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
    # Nota: En tu SQL se llama 'he_calendario_especial', pero usaremos cat_feriados por estándar
    __tablename__ = 'he_calendario_especial' 
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, unique=True, nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    es_irrenunciable = db.Column(db.Boolean, default=False)

class TipoHaber(db.Model):
    __tablename__ = 'config_tipo_haberes'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True)
    nombre = db.Column(db.String(150), nullable=False)
    es_imponible = db.Column(db.Boolean, default=True)
    es_tributable = db.Column(db.Boolean, default=True)

# --- DEMOGRÁFICOS Y CONFIG ---
class Sexo(db.Model):
    __tablename__ = 'cat_sexo'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50), nullable=False)

class NivelEstudio(db.Model):
    __tablename__ = 'cat_nivel_estudios'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50), nullable=False)

class Autoridad(db.Model):
    __tablename__ = 'cfg_autoridades_firmantes'
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(12))
    cargo = db.Column(db.String(100), nullable=False)
    decreto_nombramiento = db.Column(db.String(100))
    nombre = db.Column('firma_linea_1', db.String(150), nullable=False) # Alias para Python