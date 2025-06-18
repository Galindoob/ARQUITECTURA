import os
import re
import uuid
import shutil
from pymongo import MongoClient

# Conexión a MongoDB local
cliente = MongoClient("mongodb://localhost:27017")
db = cliente["almacenamiento"]

# Colecciones a usar
lugares_col = db["lugares"]
direcciones_col = db["direcciones"]
georeferencias_col = db["georeferencias"]

# Crear carpeta "procesados" si no existe
if not os.path.exists("procesados"):
    os.makedirs("procesados")

# Buscar todos los archivos .txt en la carpeta actual
archivos_txt = [f for f in os.listdir() if f.endswith(".txt") and os.path.isfile(f)]

# Procesar cada archivo
for archivo in archivos_txt:
    print(f"\n📄 Procesando archivo: {archivo}")

    # Verifica que el archivo tenga líneas con punto y coma (;) para asegurarse que es formato de lugares
    try:
        with open(archivo, "r", encoding="latin-1") as file:
            lineas_crudas = file.readlines()
        if not any(";" in linea for linea in lineas_crudas):
            print(f"⛔ Archivo ignorado por no tener formato de lugares: {archivo}")
            continue

        # Limpiar líneas y saltar encabezado
        lineas = [line.strip() for line in lineas_crudas[1:] if line.strip()]

        for linea in lineas:
            try:
                # Separar datos
                nombre, direccion_completa, geo = linea.split(";")
                nombre = nombre.strip()
                direccion_completa = direccion_completa.strip()
                geo = geo.strip()

                # Verificar si ya existe
                if lugares_col.find_one({"nombre_lugar": nombre}):
                    print(f"⚠️ Ya existe: {nombre}")
                    continue

                # Crear ID único
                id_lugar = str(uuid.uuid4())

                # Insertar en colección Lugares
                lugares_col.insert_one({
                    "id_lugar": id_lugar,
                    "nombre_lugar": nombre
                })

                # Procesar dirección
                partes = direccion_completa.split(",")
                if len(partes) >= 4:
                    nombre_calle = partes[0].strip()
                    numero_match = re.search(r"\d+", nombre_calle)
                    numero_calle = numero_match.group() if numero_match else ""
                    nombre_calle = re.sub(r"\d+", "", nombre_calle).strip()
                    ciudad_estado = partes[1].strip() + ", " + partes[2].strip()
                    pais = partes[3].strip()
                else:
                    nombre_calle, numero_calle, ciudad_estado, pais = "", "", "", ""

                direcciones_col.insert_one({
                    "id_lugar": id_lugar,
                    "nombre_calle": nombre_calle,
                    "numero_calle": numero_calle,
                    "ciudad_estado_provincia": ciudad_estado,
                    "pais": pais
                })

                # Procesar coordenadas
                lat, lon = map(str.strip, geo.split(","))
                georeferencias_col.insert_one({
                    "id_lugar": id_lugar,
                    "latitud": lat,
                    "longitud": lon
                })

                print(f"✅ Insertado: {nombre}")

            except Exception as e:
                print(f"❌ Error en línea: {linea}")
                print(f"   Detalle: {e}")

        # Mover archivo procesado
        shutil.move(archivo, os.path.join("procesados", archivo))
        print(f"📁 Archivo movido a carpeta 'procesados/'")

    except Exception as e:
        print(f"❌ No se pudo procesar {archivo}")
        print(f"   Detalle: {e}")
