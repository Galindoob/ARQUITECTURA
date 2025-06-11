from pymongo import MongoClient  # Importa el cliente de MongoDB para establecer la conexión

try:
    # Intentar conectarse al servidor local de MongoDB
    cliente = MongoClient('mongodb://localhost:27017')  # Conecta con MongoDB que corre localmente en el puerto por defecto (27017)

    # Acceder (o crear si no existe) la base de datos 'almacenamiento'
    db = cliente['almacenamiento']  # Selecciona la base de datos llamada 'almacenamiento'

    # Mostrar las colecciones existentes (puede estar vacío si aún no se insertan datos)
    print("✅ Conexión exitosa. Colecciones disponibles:")
    print(db.list_collection_names())  # Imprime en pantalla todas las colecciones dentro de la base 'almacenamiento'

except Exception as e:
    # Si ocurre un error al conectarse, lo muestra en consola
    print("❌ Error de conexión con MongoDB:")
    print(e)  # Imprime el mensaje de error para diagnóstico
