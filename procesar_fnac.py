import os
import re
import shutil
from datetime import datetime
from pymongo import MongoClient
import pandas as pd

# Conexión a MongoDB
cliente = MongoClient('mongodb://localhost:27017')
db = cliente['almacenamiento']
coleccion = db['fnac_famosos_norm']

# Crear carpeta "procesados" si no existe
if not os.path.exists("procesados"):
    os.makedirs("procesados")

# Función para convertir fechas a formato chileno
def normalizar_fecha(fecha_str):
    formatos = [
        "%Y/%m/%d", "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y",
        "%d/%m/%y", "%d-%m-%y", "%Y-%m-%d %H:%M:%S"
    ]
    for fmt in formatos:
        try:
            fecha = datetime.strptime(str(fecha_str), fmt)
            return fecha.strftime("%d/%m/%Y")
        except ValueError:
            continue
    return None

# Buscar archivos .txt y .xlsx
archivos = [f for f in os.listdir() if (f.endswith(".txt") or f.endswith(".xlsx")) and os.path.isfile(f)]

# Procesar cada archivo
for archivo in archivos:
    print(f"\n📄 Procesando archivo: {archivo}")

    try:
        registros = []

        if archivo.endswith(".txt"):
            with open(archivo, "r", encoding="utf-8") as file:
                lineas = file.readlines()
            for linea in lineas:
                linea = linea.strip()
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

                registros.append((nombre, fecha_raw))

        elif archivo.endswith(".xlsx"):
            df = pd.read_excel(archivo)
            if "Nombre" in df.columns and "Fecha Nacimiento Cruda" in df.columns:
                registros = list(zip(df["Nombre"], df["Fecha Nacimiento Cruda"]))
            else:
                print(f"❌ Archivo Excel no contiene las columnas requeridas: {archivo}")
                continue

        for nombre, fecha_raw in registros:
            print(f"🟢 Nombre: {nombre} | Fecha original: {fecha_raw}")
            fecha_normalizada = normalizar_fecha(fecha_raw)

            if fecha_normalizada:
                registro = f"{nombre} - {fecha_normalizada}"
            else:
                # Estimar año y agregar sufijos si aplica
                anio = "????"
                sufijo = ""
                anio_match = re.search(r"(\d{2,4})", str(fecha_raw))
                if anio_match:
                    anio = anio_match.group(1)
                if 'a.C.' in str(fecha_raw) or 'ac' in str(fecha_raw).lower():
                    sufijo = " a.C."
                elif 'd.C.' in str(fecha_raw) or 'dc' in str(fecha_raw).lower():
                    sufijo = " d.C."
                fecha_normalizada = f"00/00/{anio}{sufijo}"
                registro = f"{nombre} - {fecha_normalizada}"
                print(f"⚠️ Fecha estimada usada: {fecha_normalizada}")

            # Insertar solo si no existe
            if not coleccion.find_one({'registro': registro}):
                coleccion.insert_one({'registro': registro})
                print(f"✅ Insertado en MongoDB: {registro}")
            else:
                print(f"⚠️ Ya existe en MongoDB: {registro}")

        # Mover archivo procesado
        shutil.move(archivo, os.path.join("procesados", archivo))
        print(f"📁 Archivo movido a carpeta 'procesados/'")

    except Exception as e:
        print(f"❌ Error al procesar archivo {archivo}")
        print(f"   Detalle: {e}")
