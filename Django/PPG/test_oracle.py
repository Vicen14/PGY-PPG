import os
import sys

try:
    import oracledb
except Exception as e:
    print("Error: cannot import oracledb:", e)
    sys.exit(1)

# Opcional: inicializar Instant Client si lo tienes instalado (ruta en variable de entorno)
instant_client = os.environ.get("ORACLE_INSTANT_CLIENT")
if instant_client:
    try:
        oracledb.init_oracle_client(lib_dir=instant_client)
        print(f"Instant Client inicializado en: {instant_client}")
    except Exception as e:
        print("No se pudo inicializar Instant Client:", e)

# Intentar obtener parámetros desde Django si DJANGO_SETTINGS_MODULE está definido
user = password = dsn = None
if os.environ.get("DJANGO_SETTINGS_MODULE"):
    try:
        import django
        django.setup()
        from django.conf import settings
        db = settings.DATABASES.get("default", {})
        user = db.get("USER")
        password = db.get("PASSWORD")
        host = db.get("HOST") or ""
        port = db.get("PORT") or ""
        name = db.get("NAME")
        if host and port and name:
            dsn = f"{host}:{port}/{name}"
        else:
            dsn = name  # puede ser TNS/servicename
    except Exception as e:
        print("No se pudo leer configuración de Django:", e)

# Si no vienen de Django, leer desde variables de entorno
if not (user and password and dsn):
    user = user or os.environ.get("ORACLE_USER")
    password = password or os.environ.get("ORACLE_PASSWORD")
    host = os.environ.get("ORACLE_HOST")
    port = os.environ.get("ORACLE_PORT", "1521")
    service = os.environ.get("ORACLE_SERVICE")
    dsn = dsn or os.environ.get("ORACLE_DSN")
    if not dsn and host and service:
        dsn = f"{host}:{port}/{service}"

if not (user and password and dsn):
    print("Faltan parámetros de conexión. Define DJANGO_SETTINGS_MODULE correctamente o exporta ORACLE_USER, ORACLE_PASSWORD y ORACLE_DSN (o ORACLE_HOST/ORACLE_SERVICE).")
    sys.exit(2)

# Probar conexión y ejecutar una consulta simple
try:
    conn = oracledb.connect(user=user, password=password, dsn=dsn)
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM dual")
        row = cur.fetchone()
        print("Conexión OK. Resultado SELECT 1 FROM dual ->", row[0])
    conn.close()
except Exception as e:
    print("Error conectando a Oracle:", e)
    print("Si ves errores relacionados con DLL o libclntsh, instala Oracle Instant Client y configura ORACLE_INSTANT_CLIENT o llama a oracledb.init_oracle_client(lib_dir=...) antes de conectar().")