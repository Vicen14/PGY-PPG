import oracledb

try:
    # Probar con diferentes configuraciones
    connection = oracledb.connect(
        user="tu_usuario",
        password="tu_contraseña",
        dsn="localhost:1521/xe"  # Probar también con xepdb1
    )
    print("✅ Conexión exitosa!")
    connection.close()
except Exception as e:
    print(f"❌ Error: {e}")