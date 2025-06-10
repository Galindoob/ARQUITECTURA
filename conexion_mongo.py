from pymongo import MongoClient

try:
    # Intentar conectarse al servidor local de MongoDB
    cliente = MongoClient('mongodb://localhost:27017')

    # Acceder (o crear si no existe) la base de datos 'almacenamiento'
    db = cliente['almacenamiento']

    # Mostrar las colecciones existentes (puede estar vacío al inicio)
    print("✅ Conexión exitosa. Colecciones disponibles:")
    print(db.list_collection_names())

except Exception as e:
    print("❌ Error de conexión con MongoDB:")
    print(e)
