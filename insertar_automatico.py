import re                               # Permite usar expresiones regulares para limpiar texto
import os                               # Permite interactuar con archivos y carpetas del sistema
from pymongo import MongoClient         # Permite conectarse a MongoDB desde Python
from unidecode import unidecode         # Elimina tildes, eñes y otros caracteres especiales
from shutil import move                 # Permite mover archivos de carpeta

# Conectar a MongoDB local
cliente = MongoClient('mongodb://localhost:27017')  # Conecta con el servidor MongoDB local en el puerto 27017
db = cliente['almacenamiento']                      # Accede o crea la base de datos llamada 'almacenamiento'
coleccion = db['ciudades_norm']                     # Accede o crea la colección 'ciudades_norm' donde se guardan las ciudades normalizadas

# Función para normalizar ciudad
def normalizar_ciudad(nombre):
    nombre = nombre.strip().lower()                      # Elimina espacios y pasa todo a minúsculas
    nombre = unidecode(nombre)                           # Elimina tildes, eñes, diéresis, etc.
    nombre = re.sub(r"^\d+\.\s*", "", nombre)            # Elimina prefijos numéricos tipo "52. "
    return nombre.title()                                # Convierte a formato Título (ej: "buenos aires")

# Crear carpeta "procesados" si no existe
if not os.path.exists("procesados"):
    os.makedirs("procesados")                            # Crea la carpeta 'procesados' si no está creada

# Recorrer todos los archivos .txt de la carpeta actual
archivos_txt = [f for f in os.listdir() if os.path.isfile(f) and not f.endswith(".py") and f != "procesados"]

for archivo in archivos_txt:
    print(f"\n📄 Procesando archivo: {archivo}")
    insertadas = 0
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            lineas = file.readlines()                                                # Lee todas las líneas del archivo
            ciudades_limpias = set(normalizar_ciudad(linea) for linea in lineas)     # Aplica limpieza a cada línea y elimina duplicados

        for ciudad in ciudades_limpias:
            if not coleccion.find_one({'ciudad': ciudad}):                           # Solo inserta si la ciudad no existe aún
                coleccion.insert_one({'ciudad': ciudad})                             # Inserta ciudad normalizada como documento
                insertadas += 1

        print(f"✅ {insertadas} ciudades insertadas desde {archivo}.")

        # Mover archivo procesado a la carpeta 'procesados'
        move(archivo, f"procesados/{archivo}")
        print(f"📁 {archivo} movido a carpeta 'procesados/'.")

    except Exception as e:
        print(f"❌ Error con {archivo}: {e}")

# Mostrar resumen al final
total = coleccion.count_documents({})                                  # Cuenta el total de documentos en la colección
print(f"\n📊 Total de ciudades en MongoDB: {total}")

ultimas = coleccion.find().sort('_id', -1).limit(10)                   # Recupera las últimas 10 ciudades insertadas
print("🆕 Últimas ciudades insertadas:")
for ciudad in ultimas:
    print(f"- {ciudad['ciudad']}")                                      # Muestra cada ciudad insertada recientemente
