import os
import pymysql
from app import create_app

# --- CORRECCIÓN CRÍTICA DE DRIVER ---
# Esta línea es la clave: le dice a Python "Usa pymysql en lugar del driver mysql nativo que falta".
# Debe ir ANTES de crear la aplicación.
pymysql.install_as_MySQLdb()

# --- INICIALIZACIÓN ---
try:
    # Creamos la instancia de Flask usando tu fábrica
    app = create_app()
except Exception as e:
    print(f"❌ Error fatal al crear la aplicación: {e}")
    exit(1)

# --- EJECUCIÓN ---
if __name__ == '__main__':
    print("-------------------------------------------------------")
    print("✅ NEXU-MUNI 2.0 Iniciado correctamente")
    print("   Modo: DEBUG (Recarga automática activa)")
    print("   Base de Datos: MySQL conectado vía pymysql")
    print("   Servidor web: http://localhost:5000")
    print("-------------------------------------------------------")
    
    # Iniciamos el servidor en el puerto 5000
    app.run(debug=True, port=5000)