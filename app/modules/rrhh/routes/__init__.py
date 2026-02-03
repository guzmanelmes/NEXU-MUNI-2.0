from flask import Blueprint

# Definimos el Blueprint aquí
rrhh_bp = Blueprint('rrhh', __name__, url_prefix='/rrhh')

# Importamos los submódulos de rutas para registrarlos
# (Deben importarse DESPUÉS de definir rrhh_bp para evitar ciclos)
from . import funcionarios, mantenedores, organizacion, calendario