from app import create_app
from app.extensions import db
from app.modules.auth.models import Usuario, Rol
from sqlalchemy import text

# Inicializamos la app para tener acceso a la base de datos
app = create_app()

with app.app_context():
    print("--- INICIANDO CREACIÓN DE ADMIN ---")
    
    # 1. Crear o recuperar el Rol ADMIN
    rol_admin = Rol.query.filter_by(nombre='ADMIN').first()
    if not rol_admin:
        rol_admin = Rol(nombre='ADMIN', descripcion='Administrador Total')
        db.session.add(rol_admin)
        print("✅ Rol ADMIN creado.")
    else:
        print("ℹ️ El rol ADMIN ya existe.")

    # 2. Crear o actualizar el Usuario
    user = Usuario.query.filter_by(username='rguzman').first()
    if not user:
        # Creamos el usuario si no existe
        user = Usuario(username='rguzman', email='rguzman@santajuana.cl')
        user.set_password('admin123') # Genera el hash seguro
        user.roles.append(rol_admin)
        db.session.add(user)
        db.session.commit()
        print(f"✅ Usuario 'rguzman' creado.")
    else:
        # Si ya existe, solo le actualizamos la clave para estar seguros
        user.set_password('admin123')
        db.session.commit()
        print("✅ Contraseña de 'rguzman' reseteada a: admin123")

    # 3. Vincular con la Ficha de Personal (RUT)
    # Usamos SQL directo para evitar problemas de modelos cruzados por ahora
    rut_admin = '17.346.652-8'
    try:
        sql = text("UPDATE personas SET usuario_id = :uid WHERE rut = :rut")
        db.session.execute(sql, {'uid': user.id, 'rut': rut_admin})
        db.session.commit()
        print(f"✅ Usuario vinculado exitosamente al RUT {rut_admin}")
    except Exception as e:
        print(f"⚠️ No se pudo vincular al RUT (¿El RUT existe en la tabla personas?): {e}")

    print("\n🚀 LISTO: Ahora puedes ingresar en http://localhost:5000/auth/login")