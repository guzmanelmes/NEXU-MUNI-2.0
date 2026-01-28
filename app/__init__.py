from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config # Asegúrate de tener tu archivo config.py

# Inicializamos las extensiones fuera de la función factory
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(Config)

    # Inicializar extensiones con la app
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configuración de Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicie sesión para acceder.'

    # Importar el modelo de Usuario para el LoginManager
    from app.modules.auth.models import Usuario # Asumimos que tendrás un módulo auth
    
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # --- REGISTRO DE BLUEPRINTS (MÓDULOS) ---
    
    # 1. Módulo de Autenticación (Login/Logout)
    # (Debes crear este módulo o ajustar la ruta si ya lo tienes)
    from app.modules.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    # 2. Módulo de Recursos Humanos (EL QUE CREAMOS RECIÉN)
    from app.modules.rrhh.routes import rrhh_bp
    app.register_blueprint(rrhh_bp)

    # Ruta raíz redirige al login o al dashboard de RRHH
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    # Crear tablas si no existen (Solo para desarrollo)
    with app.app_context():
        db.create_all()

    return app