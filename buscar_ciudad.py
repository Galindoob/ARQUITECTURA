from pymongo import MongoClient
from unidecode import unidecode

# Conectar a MongoDB local
cliente = MongoClient('mongodb://localhost:27017')
db = cliente['almacenamiento']
coleccion = db['ciudades_norm']

# Función para normalizar como en el resto del sistema
def normalizar_ciudad(nombre):
    nombre = nombre.strip().lower()
    nombre = unidecode(nombre)
    return nombre.title()

# Solicitar ciudad al usuario
entrada = input("🔍 Ingrese el nombre de la ciudad a buscar: ")
ciudad_normalizada = normalizar_ciudad(entrada)

# Buscar en MongoDB
resultado = coleccion.find_one({'ciudad': ciudad_normalizada})

# Mostrar resultado
if resultado:
    print(f"✅ La ciudad '{ciudad_normalizada}' se encuentra en la base de datos.")
else:
    print(f"❌ La ciudad '{ciudad_normalizada}' NO está en la base de datos.")
