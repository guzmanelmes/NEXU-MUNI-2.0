# app/modules/rrhh/models/__init__.py

# 1. Catálogos Globales (Listas simples)
from .globales import (
    Banco, AFP, Salud, Estamento, Feriado, 
    Sexo, NivelEstudio, Autoridad, TipoHaber
)

# 2. Organización (Jerarquía Municipal)
from .organizacion import Unidad

# 3. Personas (Funcionarios y sus datos)
# ELIMINAMOS Nombramiento de aquí
from .funcionarios import Persona, PersonaArchivo, HistorialAcademico

# 4. Contratos (Vínculos laborales)
# AGREGAMOS Nombramiento aquí
from .contratos import Nombramiento, ContratoHonorario, Programa