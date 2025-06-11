# Importar las librerías necesarias
from pymongo import MongoClient           # Permite conectarse y operar con MongoDB desde Python
from unidecode import unidecode           # Permite eliminar tildes, eñes y otros caracteres especiales

# Conexión a MongoDB local
cliente = MongoClient('mongodb://localhost:27017')  # Establece conexión al servidor de MongoDB que corre localmente
db = cliente['almacenamiento']                      # Selecciona (o crea si no existe) la base de datos 'almacenamiento'
coleccion = db['ciudades_norm']                     # Selecciona (o crea) la colección 'ciudades_norm' para almacenar las ciudades

# Función para limpiar y normalizar cada nombre de ciudad
def normalizar_ciudad(nombre):
    nombre = nombre.strip().lower()        # Elimina espacios alrededor y pasa todo a minúsculas
    nombre = unidecode(nombre)             # Elimina tildes, eñes, diéresis y otros caracteres especiales
    return nombre.title()                  # Convierte a Formato Título (ej: "buenos aires" → "Buenos Aires")

# Solicita al usuario el nombre del archivo .txt a cargar
nombre_archivo = input("Nombre del archivo .txt (ej: ciudades_nuevas.txt): ")

# Abre el archivo indicado por el usuario
with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
    lineas = archivo.readlines()                                            # Lee todas las líneas del archivo como una lista
    ciudades_limpias = set(normalizar_ciudad(linea) for linea in lineas)   # Aplica normalización y elimina duplicados usando un set

# Inserta cada ciudad en MongoDB solo si no está ya registrada
insertadas = 0                                            # Contador para saber cuántas ciudades se insertan
for ciudad in ciudades_limpias:                           # Recorre todas las ciudades normalizadas y únicas
    if not coleccion.find_one({'ciudad': ciudad}):        # Verifica si la ciudad ya existe en la base
        coleccion.insert_one({'ciudad': ciudad})          # Si no existe, la inserta como nuevo documento
        insertadas += 1                                   # Suma 1 al contador de ciudades insertadas

# Muestra resultado final por pantalla
print(f"✅ {insertadas} ciudades insertadas en MongoDB.")  # Imprime cuántas ciudades nuevas se agregaron
