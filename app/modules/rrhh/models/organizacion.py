# app/modules/rrhh/models/organizacion.py
from app.extensions import db

class Unidad(db.Model):
    __tablename__ = 'cat_unidades'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    sigla = db.Column(db.String(20))
    tipo = db.Column(db.Enum('DIRECCION', 'DEPARTAMENTO', 'UNIDAD', 'OFICINA'), nullable=False)
    
    # Relación Jerárquica (Padre/Hijo)
    padre_id = db.Column(db.Integer, db.ForeignKey('cat_unidades.id'), nullable=True)
    
    # Esto permite hacer unidad.sub_unidades para ver quién depende de ella
    sub_unidades = db.relationship('Unidad', 
                                   backref=db.backref('padre', remote_side=[id]),
                                   lazy='dynamic')

    def __repr__(self):
        return f"<{self.tipo}: {self.sigla or self.nombre}>"