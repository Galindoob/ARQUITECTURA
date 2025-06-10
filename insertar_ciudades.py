from pymongo import MongoClient
from unidecode import unidecode

# Conectar a MongoDB local
cliente = MongoClient('mongodb://localhost:27017')
db = cliente['almacenamiento']
coleccion = db['ciudades_norm']

# Función para normalizar cada nombre
def normalizar_ciudad(nombre):
    nombre = nombre.strip().lower()
    nombre = unidecode(nombre)  # quita tildes, eñes, etc.
    return nombre.title()       # convierte a Formato Título

# Leer archivo
nombre_archivo = input("Nombre del archivo .txt (ej: ciudades_nuevas.txt): ")
with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
    lineas = archivo.readlines()
    ciudades_limpias = set(normalizar_ciudad(linea) for linea in lineas)

# Insertar ciudades si no existen
insertadas = 0
for ciudad in ciudades_limpias:
    if not coleccion.find_one({'ciudad': ciudad}):
        coleccion.insert_one({'ciudad': ciudad})
        insertadas += 1

print(f"✅ {insertadas} ciudades insertadas en MongoDB.")
