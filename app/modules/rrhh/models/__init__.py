# Este archivo permite importar todos los modelos desde 'app.modules.rrhh.models'
# sin tener que saber en qué archivo específico se encuentran.

# 1. Importamos Mantenedores Globales y Catálogos
from .globales import (
    Banco, 
    AFP, 
    Salud, 
    Estamento, 
    Feriado, 
    Sexo, 
    NivelEstudio, 
    Autoridad, 
    TipoHaber
)

# 2. Importamos la Organización (Jerarquía)
from .organizacion import Unidad

# 3. Importamos los Modelos de Funcionarios (Personal)
from .funcionarios import (
    Persona, 
    PersonaArchivo, 
    Nombramiento
)