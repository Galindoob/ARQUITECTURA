import re
import os
from pymongo import MongoClient
from unidecode import unidecode
from shutil import move


# Conectar a MongoDB local
cliente = MongoClient('mongodb://localhost:27017')
db = cliente['almacenamiento']
coleccion = db['ciudades_norm']

# Función para normalizar ciudad
def normalizar_ciudad(nombre):
    nombre = nombre.strip().lower()
    nombre = unidecode(nombre)
    nombre = re.sub(r"^\d+\.\s*", "", nombre)  # elimina números tipo "52. "
    return nombre.title()

# Crear carpeta "procesados" si no existe
if not os.path.exists("procesados"):
    os.makedirs("procesados")

# Recorrer archivos .txt
archivos_txt = [f for f in os.listdir() if f.endswith(".txt")]

for archivo in archivos_txt:
    print(f"\n📄 Procesando archivo: {archivo}")
    insertadas = 0
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            lineas = file.readlines()
            ciudades_limpias = set(normalizar_ciudad(linea) for linea in lineas)

        for ciudad in ciudades_limpias:
            if not coleccion.find_one({'ciudad': ciudad}):
                coleccion.insert_one({'ciudad': ciudad})
                insertadas += 1

        print(f"✅ {insertadas} ciudades insertadas desde {archivo}.")

        # Mover a carpeta "procesados"
        move(archivo, f"procesados/{archivo}")
        print(f"📁 {archivo} movido a carpeta 'procesados/'.")

    except Exception as e:
        print(f"❌ Error con {archivo}: {e}")

# Mostrar resumen al final
total = coleccion.count_documents({})
print(f"\n📊 Total de ciudades en MongoDB: {total}")

ultimas = coleccion.find().sort('_id', -1).limit(10)
print("🆕 Últimas ciudades insertadas:")
for ciudad in ultimas:
    print(f"- {ciudad['ciudad']}")
