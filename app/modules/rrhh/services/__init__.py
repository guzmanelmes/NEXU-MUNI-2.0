# app/modules/rrhh/services/__init__.py

# 1. Servicios Globales (Bancos, AFP, Salud, Estamentos, Feriados, Catálogos)
from .globales_service import (
    # Bancos
    crear_banco, obtener_bancos, obtener_banco_por_id, actualizar_banco, eliminar_banco,
    # AFP
    crear_afp, obtener_afps, obtener_afp_por_id, actualizar_afp, eliminar_afp,
    # Salud
    crear_salud, obtener_salud, obtener_salud_por_id, actualizar_salud, eliminar_salud,
    # Estamentos
    crear_estamento, obtener_estamentos, actualizar_estamento, eliminar_estamento,
    # Feriados
    crear_feriado, obtener_feriados, eliminar_feriado,
    # Autoridades
    crear_autoridad, obtener_autoridades, eliminar_autoridad,
    # Catálogos Simples (Sexo, Estudio, Haber)
    crear_genero, obtener_generos,
    crear_nivel_estudio, obtener_niveles_estudio,
    crear_tipo_haber, obtener_tipos_haberes
)

# 2. Servicios de Organización (Unidades/Departamentos)
from .organizacion_service import (
    crear_unidad, obtener_unidades, eliminar_unidad
)

# 3. Servicios de Funcionarios (Personas, Archivos)
from .funcionarios_service import (
    actualizar_foto_perfil, guardar_documento_digital
)

# 4. Servicios de Contratos (Nombramientos)
from .contratos_service import (
    crear_nombramiento
)