import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Clave secreta para sesiones (login)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu_clave_secreta_dev'
    
    # --- BASE DE DATOS ---
    # Usamos mysql+pymysql para compatibilidad total en Windows
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/NEXU_MUNI_DB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # Muestra las consultas SQL en consola (útil para debug)

    # --- CONFIGURACIÓN DE ARCHIVOS (NUEVO) ---
    # 1. Obtenemos la ruta de la carpeta raíz del proyecto (subiendo un nivel desde 'config')
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    # 2. Definimos dónde se guardarán las fotos y documentos: app/static/uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
    
    # 3. Límite de tamaño: 16 Megabytes máx por archivo
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024