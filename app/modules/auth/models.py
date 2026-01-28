from app.extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Tabla intermedia (Muchos a Muchos)
usuario_roles = db.Table('auth_usuario_roles',
    db.Column('usuario_id', db.Integer, db.ForeignKey('auth_usuarios.id', ondelete='CASCADE'), primary_key=True),
    db.Column('rol_id', db.Integer, db.ForeignKey('auth_roles.id', ondelete='CASCADE'), primary_key=True)
)

class Rol(db.Model):
    __tablename__ = 'auth_roles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(255))

    def __repr__(self):
        return f'<Rol {self.nombre}>'

class Usuario(UserMixin, db.Model):
    __tablename__ = 'auth_usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    
    # Relación con Roles
    roles = db.relationship('Rol', secondary=usuario_roles, backref=db.backref('usuarios', lazy='dynamic'))

    # Relación con Ficha de Personal (RRHH)
    # Esto es vital: nos permite acceder a usuario.ficha_personal.nombres
    ficha_personal = db.relationship('Persona', backref='usuario_sistema', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # Verifica si el usuario tiene un rol específico (Ej: usuario.tiene_rol('ADMIN'))
    def tiene_rol(self, nombre_rol):
        return any(rol.nombre == nombre_rol for rol in self.roles)

# Configuración obligatoria para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))