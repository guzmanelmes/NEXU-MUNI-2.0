from flask import Flask, redirect, url_for
# CAMBIO IMPORTANTE: Importamos las instancias desde extensions.py
from app.extensions import db, login_manager 
from config.settings import Config

def create_app():
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(Config)

    # Inicializar las extensiones que importamos
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configuración de Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicie sesión para acceder.'

    # Importar modelo de Usuario (dentro de la función para evitar ciclos)
    from app.modules.auth.models import Usuario
    
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # --- REGISTRO DE BLUEPRINTS (MÓDULOS) ---
    
    # 1. Autenticación
    from app.modules.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    # 2. Recursos Humanos
    from app.modules.rrhh.routes import rrhh_bp
    app.register_blueprint(rrhh_bp)

    # 3. Módulo Core (Dashboard)
    from app.modules.core.routes import core_bp
    app.register_blueprint(core_bp)
    
    # Redirección inicial
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    # Crear tablas (Solo desarrollo)
    with app.app_context():
        db.create_all()

    return app