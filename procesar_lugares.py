import os                          # Módulo para manejo de archivos y rutas
import re                          # Módulo de expresiones regulares para extraer números o limpiar texto
import uuid                        # Para generar identificadores únicos
from pymongo import MongoClient    # Cliente para conectarse y trabajar con MongoDB

# Conexión a MongoDB local
cliente = MongoClient("mongodb://localhost:27017")  # Se conecta al servidor MongoDB que corre en localhost
db = cliente["almacenamiento"]                      # Se selecciona (o crea) la base de datos llamada "almacenamiento"

# Definición de las colecciones en donde se dividirán los datos
lugares_col = db["lugares"]                         # Tabla para almacenar los nombres de los lugares
direcciones_col = db["direcciones"]                 # Tabla para almacenar información de dirección
georeferencias_col = db["georeferencias"]           # Tabla para almacenar coordenadas geográficas

# Archivo de entrada (debe estar en la misma carpeta que el script)
archivo = "DATOS3.txt"

# Lectura del archivo, usando codificación latin-1 (compatible con caracteres especiales y acentos)
# Se omite la primera línea (asumiendo que es un encabezado)
with open(archivo, "r", encoding="latin-1") as file:
    lineas = [line.strip() for line in file.readlines()[1:] if line.strip()]  # Elimina líneas vacías y espacios extra

# Procesar cada línea del archivo
for linea in lineas:
    try:
        # Separar la línea en nombre, dirección y georeferencia
        nombre, direccion_completa, geo = linea.split(";")
        nombre = nombre.strip()
        direccion_completa = direccion_completa.strip()
        geo = geo.strip()

        # Revisar si el lugar ya fue insertado previamente en la colección
        if lugares_col.find_one({"nombre_lugar": nombre}):
            print(f"⚠️ Ya existe: {nombre}")
            continue  # Saltar al siguiente si ya existe

        # Generar un identificador único para enlazar entre tablas
        id_lugar = str(uuid.uuid4())

        # Insertar en la colección de Lugares
        lugares_col.insert_one({
            "id_lugar": id_lugar,
            "nombre_lugar": nombre
        })

        # Procesar los componentes de la dirección
        partes = direccion_completa.split(",")  # Separar por coma
        if len(partes) >= 4:
            nombre_calle = partes[0].strip()                                # Ej: "Av. Main Street 123"
            numero_calle_match = re.search(r"\d+", nombre_calle)            # Buscar número dentro del string
            numero_calle = numero_calle_match.group() if numero_calle_match else ""  # Si hay número, lo extrae
            nombre_calle = re.sub(r"\d+", "", nombre_calle).strip()         # Remueve los dígitos del nombre de calle
            ciudad_estado = partes[1].strip() + ", " + partes[2].strip()    # Combina ciudad y estado
            pais = partes[3].strip()                                        # Toma el país
        else:
            # Si la dirección no tiene suficiente información, se dejan los campos vacíos
            nombre_calle, numero_calle, ciudad_estado, pais = "", "", "", ""

        # Insertar en la colección de Direcciones
        direcciones_col.insert_one({
            "id_lugar": id_lugar,
            "nombre_calle": nombre_calle,
            "numero_calle": numero_calle,
            "ciudad_estado_provincia": ciudad_estado,
            "pais": pais
        })

        # Procesar coordenadas geográficas (esperadas en formato: latitud,longitud)
        lat, lon = map(str.strip, geo.split(","))  # Elimina espacios extra
        georeferencias_col.insert_one({
            "id_lugar": id_lugar,
            "latitud": lat,
            "longitud": lon
        })

        print(f"✅ Insertado: {nombre}")  # Confirmación en consola

    except Exception as e:
        # Manejo de errores en caso de líneas mal formateadas
        print(f"❌ Error en línea: {linea}")
        print(f"   Detalle: {e}")
