import os
import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask
from config.settings import Config
from app.extensions import db, login_manager

def create_app():
    # --- CORRECCIÓN DE RUTAS ---
    # Calculamos la ruta absoluta a la carpeta 'templates' dentro de 'app'
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')

    # Iniciamos Flask diciéndole explícitamente dónde están las carpetas
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    
    app.config.from_object(Config)

    # Iniciar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Por favor inicie sesión para acceder."
    login_manager.login_message_category = "warning"

    # Registrar Módulos
    from app.modules.auth.routes import auth_bp
    from app.modules.core.routes import core_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(core_bp)

    return app