from flask import Blueprint

# Definimos el Blueprint principal (sin prefijo, es la raíz del sitio)
core_bp = Blueprint('core', __name__)

@core_bp.route('/')
def index():
    return """
    <div style="font-family: sans-serif; text-align: center; padding: 50px;">
        <h1 style="color: #2563eb;">Bienvenido a NEXU-MUNI 2.0 🚀</h1>
        <p>Conexión exitosa a la base de datos y sistema modular activo.</p>
        <br>
        <a href="/auth/login" style="background-color: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Ir al Login</a>
    </div>
    """