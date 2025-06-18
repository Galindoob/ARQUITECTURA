import os
import re
from datetime import datetime
from pymongo import MongoClient
import shutil

# Conexión a MongoDB
cliente = MongoClient('mongodb://localhost:27017')
db = cliente['almacenamiento']
coleccion = db['fnac_famosos_norm']

# Crear carpeta "procesados" si no existe
if not os.path.exists("procesados"):
    os.makedirs("procesados")

# Función para convertir fechas estándar
def normalizar_fecha(fecha_str):
    formatos = ["%Y/%m/%d", "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y", "%d-%m-%y"]
    for fmt in formatos:
        try:
            fecha = datetime.strptime(fecha_str, fmt)
            return fecha.strftime("%d/%m/%Y")
        except ValueError:
            continue
    return None

# Buscar todos los archivos .txt que no están en "procesados"
archivos_txt = [f for f in os.listdir() if f.endswith(".txt") and os.path.isfile(f)]

for archivo in archivos_txt:
    print(f"\n📄 Procesando archivo: {archivo}")

    try:
        with open(archivo, "r", encoding="utf-8") as file:
            lineas = file.readlines()

        for linea in lineas:
            linea = linea.strip()

            # Intentar separar por guion o por coma
            match_guion = re.match(r"\d+\.\s*(.+?)\s*-\s*(.+)", linea)
            match_simple = re.match(r"(.+?),\s*(.+)", linea)

            if match_guion:
                nombre = match_guion.group(1).strip()
                fecha_raw = match_guion.group(2).strip()
            elif match_simple:
                nombre = match_simple.group(1).strip()
                fecha_raw = match_simple.group(2).strip()
            else:
                print(f"❌ Línea no válida: {linea}")
                continue

            print(f"🟢 Nombre: {nombre} | Fecha original: {fecha_raw}")

            fecha_normalizada = normalizar_fecha(fecha_raw)

            if fecha_normalizada:
                registro = f"{nombre} - {fecha_normalizada}"
            else:
                # Buscar año y sufijo a.C. o d.C.
                anio = "????"
                sufijo = ""
                anio_match = re.search(r"(\d{2,4})", fecha_raw)
                if anio_match:
                    anio = anio_match.group(1)
                if 'a.C.' in fecha_raw or 'ac' in fecha_raw.lower():
                    sufijo = " a.C."
                elif 'd.C.' in fecha_raw or 'dc' in fecha_raw.lower():
                    sufijo = " d.C."
                fecha_normalizada = f"00/00/{anio}{sufijo}"
                registro = f"{nombre} - {fecha_normalizada}"
                print(f"⚠️ Fecha estimada usada: {fecha_normalizada}")

            if not coleccion.find_one({'registro': registro}):
                coleccion.insert_one({'registro': registro})
                print(f"✅ Insertado en MongoDB: {registro}")
            else:
                print(f"⚠️ Ya existe en MongoDB: {registro}")

        # Mover archivo a "procesados"
        shutil.move(archivo, os.path.join("procesados", archivo))
        print(f"📁 Archivo movido a carpeta 'procesados/'")

    except Exception as e:
        print(f"❌ Error al procesar archivo {archivo}")
        print(f"   Detalle: {e}")
