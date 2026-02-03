# app/modules/rrhh/services/__init__.py

# 1. Mantenedores Globales (Bancos, AFP, Salud, Estamentos, Catálogos y CONTRATOS)
from .mantenedores_service import (
    # Bancos
    crear_banco, obtener_bancos, obtener_banco_por_id, actualizar_banco, eliminar_banco,
    # AFP
    crear_afp, obtener_afps, obtener_afp_por_id, actualizar_afp, eliminar_afp,
    # Salud
    crear_salud, obtener_salud, obtener_salud_por_id, actualizar_salud, eliminar_salud,
    # Estamentos
    crear_estamento, obtener_estamentos, actualizar_estamento, eliminar_estamento,
    # Catálogos Simples (GÉNEROS Y ESTUDIOS)
    crear_genero, obtener_generos, obtener_genero_por_id, actualizar_genero, eliminar_genero,
    crear_nivel_estudio, obtener_niveles_estudio, obtener_nivel_estudio_por_id, actualizar_nivel_estudio, eliminar_nivel_estudio,
    # Tipos de Contrato (Agregado para solucionar el error)
    crear_tipo_contrato, obtener_tipos_contrato, obtener_tipo_contrato_por_id, actualizar_tipo_contrato, eliminar_tipo_contrato
)

# 2. Remuneraciones (Haberes, Fórmulas)
from .remuneraciones_service import (
    crear_tipo_haber, obtener_tipos_haberes, 
    obtener_tipo_haber_por_id, actualizar_tipo_haber, eliminar_tipo_haber
)

# 3. Calendario (Feriados, Asistencia)
from .calendario_service import (
    crear_feriado, obtener_feriados, obtener_feriado_por_id, actualizar_feriado, eliminar_feriado
)

# 4. Organización (Unidades y Autoridades)
from .organizacion_service import (
    # Unidades
    crear_unidad, obtener_unidades, obtener_unidad_por_id, actualizar_unidad, eliminar_unidad,
    # Autoridades
    crear_autoridad, obtener_autoridades, obtener_autoridad_por_id, actualizar_autoridad, eliminar_autoridad
)

# 5. Funcionarios
from .funcionarios_service import (
    actualizar_foto_perfil, 
    guardar_documento_digital,
    buscar_persona_por_rut
)

# 6. Contratos
from .contratos_service import (
    crear_nombramiento
)