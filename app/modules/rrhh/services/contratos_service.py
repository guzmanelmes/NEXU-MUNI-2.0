from app.extensions import db
# Importamos solo lo que realmente existe en models/contratos.py
from app.modules.rrhh.models.contratos import Nombramiento, ContratoHonorario
# Si necesitas usar Programa, ahora se importa desde globales
from app.modules.rrhh.models.globales import Programa

def crear_nombramiento(persona_id, calidad, estamento_id, grado, fecha_inicio):
    # Lógica futura para crear contratos
    pass