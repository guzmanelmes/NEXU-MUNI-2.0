# app/modules/rrhh/models/__init__.py

# 1. Catálogos Globales (Listas simples + PROGRAMA está aquí ahora)
from .globales import (
    Banco, AFP, Salud, Estamento, Feriado, 
    Sexo, NivelEstudio, Autoridad, TipoHaber,
    # --- IMPORTANTE: Programa, Cuenta y TipoContrato vienen de globales ---
     CuentaPresupuestaria, TipoContrato
)

# 2. Organización (Jerarquía Municipal)
from .organizacion import Unidad

# 3. Personas (Funcionarios y sus datos)
from .funcionarios import Persona, PersonaArchivo, HistorialAcademico

# 4. Contratos (Vínculos laborales)
# ELIMINA 'Programa' de esta línea. Solo deja Nombramiento y ContratoHonorario.
from .contratos import Nombramiento, ContratoHonorario