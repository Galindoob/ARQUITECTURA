from pymongo import MongoClient           # Importa el cliente de MongoDB para conectarse desde Python
from unidecode import unidecode           # Importa la función que elimina tildes, eñes y otros caracteres especiales

# Conectar a MongoDB local
cliente = MongoClient('mongodb://localhost:27017')  # Establece conexión con el servidor MongoDB local
db = cliente['almacenamiento']                      # Accede (o crea si no existe) la base de datos llamada 'almacenamiento'
coleccion = db['ciudades_norm']                     # Accede (o crea) la colección 'ciudades_norm' donde están las ciudades normalizadas

# Función para normalizar como en el resto del sistema
def normalizar_ciudad(nombre):
    nombre = nombre.strip().lower()       # Elimina espacios al inicio y final, y convierte a minúsculas
    nombre = unidecode(nombre)            # Elimina tildes, diéresis, eñes y caracteres especiales
    return nombre.title()                 # Convierte el texto a formato Título (ej: "santiago" → "Santiago")

# Solicitar ciudad al usuario
entrada = input("🔍 Ingrese el nombre de la ciudad a buscar: ")       # Pide al usuario que ingrese el nombre de una ciudad
ciudad_normalizada = normalizar_ciudad(entrada)                      # Aplica la función de limpieza y normalización

# Buscar en MongoDB
resultado = coleccion.find_one({'ciudad': ciudad_normalizada})       # Busca en la base de datos si existe esa ciudad

# Mostrar resultado
if resultado:
    print(f"✅ La ciudad '{ciudad_normalizada}' se encuentra en la base de datos.")  # Muestra mensaje si existe
else:
    print(f"❌ La ciudad '{ciudad_normalizada}' NO está en la base de datos.")        # Muestra mensaje si no se encuentra
