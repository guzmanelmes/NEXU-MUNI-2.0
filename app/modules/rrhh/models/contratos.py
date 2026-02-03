# app/modules/rrhh/models/contratos.py
from app.extensions import db

class Nombramiento(db.Model):
    __tablename__ = 'nombramientos'
    
    id = db.Column(db.Integer, primary_key=True)
    persona_id = db.Column(db.String(12), db.ForeignKey('personas.rut'))
    
    # Detalles Contractuales
    calidad_juridica = db.Column(db.String(50)) # PLANTA, CONTRATA
    estamento_id = db.Column(db.Integer, db.ForeignKey('cat_estamentos.id'))
    unidad_id = db.Column(db.Integer, db.ForeignKey('cat_unidades.id'))
    grado = db.Column(db.Integer)
    
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    estado = db.Column(db.String(20)) # VIGENTE, FINALIZADO

    # Relaciones
    estamento = db.relationship('Estamento')
    unidad = db.relationship('Unidad')

# --- ¡CORRECTO! Aquí YA NO DEBE ESTAR la clase Programa ---

class ContratoHonorario(db.Model):
    __tablename__ = 'contratos_honorarios'
    
    id = db.Column(db.Integer, primary_key=True)
    persona_id = db.Column(db.String(12), db.ForeignKey('personas.rut'))
    programa_id = db.Column(db.Integer, db.ForeignKey('programas.id')) # Apunta a la tabla correcta en globales
    
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    monto_total = db.Column(db.Integer)
    estado = db.Column(db.Enum('BORRADOR','VIGENTE','FINALIZADO'), default='BORRADOR')
    
    # SQLAlchemy encontrará el modelo 'Programa' automáticamente desde los metadatos globales
    programa = db.relationship('Programa')