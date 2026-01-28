# app/modules/rrhh/models/funcionarios.py
from app.extensions import db
from datetime import datetime

class Persona(db.Model):
    __tablename__ = 'personas'
    
    rut = db.Column(db.String(12), primary_key=True)
    nombres = db.Column(db.String(100))
    apellido_paterno = db.Column(db.String(100))
    apellido_materno = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(255))
    
    # Campos Sistema
    usuario_id = db.Column(db.Integer, db.ForeignKey('auth_usuarios.id'))
    foto_perfil = db.Column(db.String(255))
    
    # Claves Foráneas (Relaciones con Globales)
    banco_id = db.Column(db.Integer, db.ForeignKey('cat_bancos.id'))
    sexo_id = db.Column(db.Integer, db.ForeignKey('cat_sexo.id'))
    nivel_estudios_id = db.Column(db.Integer, db.ForeignKey('cat_nivel_estudios.id'))
    
    # Relaciones Directas (Objetos)
    sexo = db.relationship('Sexo', backref='personas')
    nivel_estudio = db.relationship('NivelEstudio', backref='personas')
    banco = db.relationship('Banco', backref='personas')

    # Relaciones Hijas (Lo que tiene la persona)
    # Nota: Usamos strings en lazy='dynamic' para evitar importaciones circulares
    nombramientos = db.relationship('Nombramiento', backref='funcionario', lazy=True)
    contratos_honorarios = db.relationship('ContratoHonorario', backref='funcionario', lazy=True)
    archivos = db.relationship('PersonaArchivo', backref='propietario', lazy=True)

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno}"

class PersonaArchivo(db.Model):
    __tablename__ = 'personas_archivos'
    id = db.Column(db.Integer, primary_key=True)
    rut_persona = db.Column(db.String(12), db.ForeignKey('personas.rut'))
    nombre_visible = db.Column(db.String(150), nullable=False)
    nombre_archivo = db.Column(db.String(255), nullable=False)
    tipo_documento = db.Column(db.String(50))
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)

class HistorialAcademico(db.Model):
    __tablename__ = 'historial_academico'
    id = db.Column(db.Integer, primary_key=True)
    rut_persona = db.Column(db.String(12), db.ForeignKey('personas.rut'))
    nombre_titulo = db.Column(db.String(150))
    institucion = db.Column(db.String(150))
    fecha_titulacion = db.Column(db.Date)