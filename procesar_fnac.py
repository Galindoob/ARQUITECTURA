# Importación de librerías necesarias
import os                     # Para interactuar con archivos y carpetas del sistema
import re                     # Para trabajar con expresiones regulares (extracción de datos)
from datetime import datetime # Para manejo y conversión de fechas
from pymongo import MongoClient # Para conexión y operaciones con MongoDB
import shutil                 # Para mover archivos entre carpetas

# Conexión a la base de datos MongoDB local
cliente = MongoClient('mongodb://localhost:27017')  # Dirección estándar de un servidor MongoDB local
db = cliente['almacenamiento']                      # Base de datos llamada "almacenamiento"
coleccion = db['fnac_famosos_norm']                 # Colección específica donde se guardarán los registros

# Crear carpeta "procesados" si no existe (para mover archivos ya trabajados)
if not os.path.exists("procesados"):
    os.makedirs("procesados")

# Función para intentar convertir una fecha en formato estándar a formato chileno (dd/mm/yyyy)
def normalizar_fecha(fecha_str):
    formatos = [  # Lista de posibles formatos a reconocer
        "%Y/%m/%d", "%Y-%m-%d",
        "%d/%m/%Y", "%d-%m-%Y",
        "%d/%m/%y", "%d-%m-%y"
    ]
    for fmt in formatos:
        try:
            fecha = datetime.strptime(fecha_str, fmt)  # Intenta convertir la cadena con ese formato
            return fecha.strftime("%d/%m/%Y")           # Devuelve la fecha normalizada en formato chileno
        except ValueError:
            continue                                   # Si falla, sigue probando con el siguiente formato
    return None  # Si no se logró convertir con ningún formato

# Buscar todos los archivos .txt en el directorio actual (excluyendo subcarpetas)
archivos_txt = [f for f in os.listdir() if f.endswith(".txt") and os.path.isfile(f)]

# Iterar sobre cada archivo de texto encontrado
for archivo in archivos_txt:
    print(f"\n📄 Procesando archivo: {archivo}")

    try:
        # Abrir el archivo con codificación utf-8
        with open(archivo, "r", encoding="utf-8") as file:
            lineas = file.readlines()  # Leer todas las líneas del archivo

        # Procesar línea por línea
        for linea in lineas:
            linea = linea.strip()  # Eliminar espacios en blanco al principio y al final

            # Verifica si la línea tiene formato con guion ("1. Nombre - Fecha") o con coma ("Nombre, Fecha")
            match_guion = re.match(r"\d+\.\s*(.+?)\s*-\s*(.+)", linea)
            match_simple = re.match(r"(.+?),\s*(.+)", linea)

            # Extraer nombre y fecha con el formato que corresponda
            if match_guion:
                nombre = match_guion.group(1).strip()
                fecha_raw = match_guion.group(2).strip()
            elif match_simple:
                nombre = match_simple.group(1).strip()
                fecha_raw = match_simple.group(2).strip()
            else:
                # Si no coincide con ningún formato conocido, se reporta como inválida
                print(f"❌ Línea no válida: {linea}")
                continue

            # Mostrar en consola lo que se está procesando
            print(f"🟢 Nombre: {nombre} | Fecha original: {fecha_raw}")

            # Intentar normalizar la fecha
            fecha_normalizada = normalizar_fecha(fecha_raw)

            # Si se logró normalizar correctamente
            if fecha_normalizada:
                registro = f"{nombre} - {fecha_normalizada}"  # Formato final
            else:
                # Si no es una fecha estándar, extraer el año manualmente
                anio = "????"
                sufijo = ""
                anio_match = re.search(r"(\d{2,4})", fecha_raw)  # Buscar número de 2 a 4 dígitos
                if anio_match:
                    anio = anio_match.group(1)
                if 'a.C.' in fecha_raw or 'ac' in fecha_raw.lower():
                    sufijo = " a.C."
                elif 'd.C.' in fecha_raw or 'dc' in fecha_raw.lower():
                    sufijo = " d.C."
                fecha_normalizada = f"00/00/{anio}{sufijo}"
                registro = f"{nombre} - {fecha_normalizada}"
                print(f"⚠️ Fecha estimada usada: {fecha_normalizada}")

            # Insertar en MongoDB si el registro no existe previamente
            if not coleccion.find_one({'registro': registro}):
                coleccion.insert_one({'registro': registro})
                print(f"✅ Insertado en MongoDB: {registro}")
            else:
                print(f"⚠️ Ya existe en MongoDB: {registro}")

        # Mover el archivo a la carpeta "procesados" para no reusarlo
        shutil.move(archivo, os.path.join("procesados", archivo))
        print(f"📁 Archivo movido a carpeta 'procesados/'")

    except Exception as e:
        # Captura y muestra errores si el archivo no pudo ser procesado
        print(f"❌ Error al procesar archivo {archivo}")
        print(f"   Detalle: {e}")
