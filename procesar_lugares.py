# Importación de librerías necesarias
import os                         # Para operaciones con archivos y carpetas
import re                         # Para usar expresiones regulares (extraer datos)
import uuid                       # Para generar identificadores únicos
import shutil                     # Para mover archivos de carpeta
from pymongo import MongoClient   # Para conectarse y trabajar con MongoDB

# Establecer conexión con MongoDB local
cliente = MongoClient("mongodb://localhost:27017")  # Dirección del servidor MongoDB local
db = cliente["almacenamiento"]                      # Selecciona o crea la base de datos "almacenamiento"

# Definición de las colecciones que se usarán
lugares_col = db["lugares"]             # Colección para los lugares
direcciones_col = db["direcciones"]     # Colección para las direcciones
georeferencias_col = db["georeferencias"] # Colección para las coordenadas geográficas

# Crear carpeta "procesados" si no existe, para mover los archivos que ya fueron usados
if not os.path.exists("procesados"):
    os.makedirs("procesados")

# Buscar todos los archivos .txt que estén en la misma carpeta que este script
archivos_txt = [f for f in os.listdir() if f.endswith(".txt") and os.path.isfile(f)]

# Procesar cada archivo uno por uno
for archivo in archivos_txt:
    print(f"\n📄 Procesando archivo: {archivo}")

    try:
        # Leer contenido del archivo con codificación compatible con acentos (latin-1)
        with open(archivo, "r", encoding="latin-1") as file:
            lineas_crudas = file.readlines()

        # Verificar si el archivo tiene estructura con punto y coma (";"), necesaria para lugares
        if not any(";" in linea for linea in lineas_crudas):
            print(f"⛔ Archivo ignorado por no tener formato de lugares: {archivo}")
            continue  # Salta a siguiente archivo

        # Limpia líneas y salta encabezado (usualmente línea 0)
        lineas = [line.strip() for line in lineas_crudas[1:] if line.strip()]

        # Procesar línea por línea del archivo
        for linea in lineas:
            try:
                # Dividir la línea en nombre, dirección y coordenadas usando el separador ";"
                nombre, direccion_completa, geo = linea.split(";")
                nombre = nombre.strip()
                direccion_completa = direccion_completa.strip()
                geo = geo.strip()

                # Verificar si el lugar ya existe (por nombre exacto) para evitar duplicados
                if lugares_col.find_one({"nombre_lugar": nombre}):
                    print(f"⚠️ Ya existe: {nombre}")
                    continue

                # Crear un ID único para relacionar con las otras colecciones
                id_lugar = str(uuid.uuid4())

                # Insertar nombre del lugar en la colección "lugares"
                lugares_col.insert_one({
                    "id_lugar": id_lugar,
                    "nombre_lugar": nombre
                })

                # Procesar dirección dividiendo por coma
                partes = direccion_completa.split(",")
                if len(partes) >= 4:
                    nombre_calle = partes[0].strip()
                    numero_match = re.search(r"\d+", nombre_calle)  # Buscar número en el nombre de calle
                    numero_calle = numero_match.group() if numero_match else ""
                    nombre_calle = re.sub(r"\d+", "", nombre_calle).strip()  # Eliminar número de la calle
                    ciudad_estado = partes[1].strip() + ", " + partes[2].strip()
                    pais = partes[3].strip()
                else:
                    # Si faltan partes, se guarda vacío
                    nombre_calle, numero_calle, ciudad_estado, pais = "", "", "", ""

                # Insertar datos de dirección en su colección correspondiente
                direcciones_col.insert_one({
                    "id_lugar": id_lugar,
                    "nombre_calle": nombre_calle,
                    "numero_calle": numero_calle,
                    "ciudad_estado_provincia": ciudad_estado,
                    "pais": pais
                })

                # Procesar georeferencias (latitud y longitud)
                lat, lon = map(str.strip, geo.split(","))
                georeferencias_col.insert_one({
                    "id_lugar": id_lugar,
                    "latitud": lat,
                    "longitud": lon
                })

                # Confirmar inserción en consola
                print(f"✅ Insertado: {nombre}")

            except Exception as e:
                # Si hay un error procesando una línea individual
                print(f"❌ Error en línea: {linea}")
                print(f"   Detalle: {e}")

        # Una vez procesado el archivo, se mueve a la carpeta "procesados"
        shutil.move(archivo, os.path.join("procesados", archivo))
        print(f"📁 Archivo movido a carpeta 'procesados/'")

    except Exception as e:
        # Si hay un error general procesando el archivo completo
        print(f"❌ No se pudo procesar {archivo}")
        print(f"   Detalle: {e}")
