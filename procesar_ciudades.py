from pymongo import MongoClient
from unidecode import unidecode
import os

# Conexión a MongoDB local
cliente = MongoClient('mongodb://localhost:27017')
db = cliente['almacenamiento']
coleccion = db['ciudades_norm']

# Solicita el nombre del archivo de ciudades
nombre_archivo = input("📄 Ingrese el nombre del archivo de ciudades (ej: CIDUADES_CHILE.txt): ")

try:
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        lineas = archivo.readlines()
        # Normaliza nombres y elimina duplicados
        ciudades_limpias = set(unidecode(linea.strip().lower().title()) for linea in lineas if linea.strip())

    insertadas = 0
    for ciudad in ciudades_limpias:
        if not coleccion.find_one({'ciudad': ciudad}):
            coleccion.insert_one({'ciudad': ciudad})
            insertadas += 1

    print(f"✅ {insertadas} ciudades insertadas en MongoDB.")

except FileNotFoundError:
    print(f"❌ El archivo '{nombre_archivo}' no fue encontrado.")
except Exception as e:
    print(f"❌ Error al procesar el archivo.")
    print(f"   Detalle: {e}")
