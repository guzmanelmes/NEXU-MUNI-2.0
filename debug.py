print("--- INICIANDO DIAGNÓSTICO ---")

try:
    print("1. Importando pymysql...")
    import pymysql
    pymysql.install_as_MySQLdb()
    print("   [OK] Driver MySQL configurado.")
except Exception as e:
    print(f"   [ERROR] Falló pymysql: {e}")
    exit()

try:
    print("2. Buscando la aplicación Flask...")
    from app import create_app
    print("   [OK] Archivos de la app encontrados.")
except Exception as e:
    print(f"   [ERROR] No se pudo importar la app. Revisa app/__init__.py: {e}")
    exit()

try:
    print("3. Creando la instancia de Flask...")
    app = create_app()
    print("   [OK] Aplicación creada en memoria.")
except Exception as e:
    print(f"   [ERROR] Falló al crear la app (create_app): {e}")
    # Imprimir el error completo para ver detalles
    import traceback
    traceback.print_exc()
    exit()

print("4. Intentando levantar el servidor...")
if __name__ == '__main__':
    try:
        app.run(debug=True, port=5000)
    except Exception as e:
        print(f"   [ERROR] El servidor falló al arrancar: {e}")